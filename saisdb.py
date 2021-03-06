import psycopg2

#Connect to database
conn = psycopg2.connect("")
cur = conn.cursor()
#reset sequence with "alter sequence sais_reports_id_seq restart with 1"

def SaveObservation(LRIMOShipNo,Latitude,Longitude,AdditionalInfo,CallSign,Heading,MMSI,MovementDateTime,MovementID,ShipName,ShipType,Speed,Beam,Draught,Length,Destination,ETA,MoveStatus):
    #print str(Latitude) + " " + str(Longitude) + " " + str(MMSI) + " " + str(MovementDateTime)
    cur.execute("""INSERT INTO sais_ihs_raw (imonumber, reportedpoint, latitude, longitude, additionalinfo, callsign, heading, mmsi, reportdate, movementid, shipname, shiptype, speed, beam, draught, length, destination, eta, movestatus)
SELECT %(imo)s, ST_GeomFromText('POINT(%(lon)s %(lat)s)', 4326), %(lat)s, %(lon)s, %(addinfo)s, %(call)s, %(head)s,%(mmsi)s,
to_timestamp(%(movedt)s, 'YYYY-MM-DD HH24:MI:SS:MS'), %(moveid)s,%(ship)s,%(type)s,%(spd)s,%(beam)s,%(draught)s,%(length)s,%(dest)s,%(eta)s,%(move)s;
""", {'imo': LRIMOShipNo,'lat': Latitude,'lon': Longitude,'addinfo':AdditionalInfo,'call':CallSign.strip(),'head':Heading.strip(),'mmsi':MMSI.strip(),'movedt':MovementDateTime,
              'moveid':MovementID,'ship':ShipName.strip(),'type':ShipType.strip(),'spd':Speed,'beam':Beam,'draught':Draught,'length':Length,'dest':Destination.strip(),'eta':ETA,'move':MoveStatus.strip()})
    conn.commit()
    
'''Saves IHS SAIS observations to ihs_raw_data table from text files'''
def SaveIhsObservation(LRIMOShipNo,Latitude,Longitude,AdditionalInfo,CallSign,Heading,MMSI,MovementDateTime,MovementID,ShipName,ShipType,Speed,Beam,Draught,Length,Destination,ETA,MoveStatus):
    #print str(Latitude) + " " + str(Longitude) + " " + str(MMSI) + " " + str(MovementDateTime)
    cur.execute("""INSERT INTO ihs_raw_data (imonumber, latitude, longitude, additionalinfo, callsign, heading, mmsi, reportdate, movementid, shipname, shiptype, speed, beam, draught, length, destination, eta, movestatus)
SELECT %(imo)s, %(lat)s, %(lon)s, %(addinfo)s, %(call)s, %(head)s, %(mmsi)s,
to_timestamp(%(movedt)s, 'YYYY-MM-DD HH24:MI:SS:MS'), %(moveid)s, %(ship)s, %(type)s, %(spd)s, %(beam)s, %(draught)s, %(length)s, %(dest)s, %(eta)s, %(move)s;
""", {'imo':LRIMOShipNo, 'lat':Latitude, 'lon':Longitude, 'addinfo':AdditionalInfo, 'call':CallSign.strip(), 'head':Heading.strip(), 'mmsi':MMSI.strip(), 'movedt':MovementDateTime, 'moveid':MovementID, 'ship':ShipName.strip(), 'type':ShipType.strip(), 'spd':Speed, 'beam':Beam, 'draught':Draught, 'length':Length, 'dest':Destination.strip(), 'eta':ETA, 'move':MoveStatus.strip()})
    conn.commit()

def GetIncompleteShips():
    cur.execute("""SELECT DISTINCT(mmsi) FROM vesseldetails WHERE updatedate IS NULL LIMIT 50;""")
    rows = cur.fetchall()
    cur.close()
    conn.commit()
    return rows

def UpdateVesselDetailsFromMmsi(LRImo, Vessel, Cs, Gton, Dw, Flag, Built, Type, Status, Source, Length, Beam, MMSI):
    cur.execute("""UPDATE vesseldetails SET imo = %(imonum), name = %(vname), callsign = %(call), tonnage = %(grosston), deadweight = %(dead), flag = %(fl), yearbuilt = %(build), type = %(vtype), status = %(stat), datasource = %(ds), length=%(len), beam=%(beam), updatedate = now() WHERE mmsi = %(mmsi);""", {'imonum':LRImo, 'vname':Vessel, 'call':Cs, 'grosston':Gton, 'dead':Dw, 'fl':Flag, 'build':Built, 'vtype':Type, 'stat':Status, 'ds':Source, 'len':Length, 'beam':Beam, 'mmsi':MMSI})
    conn.commit()

def UpdateNullVesselFromMmsi(MMSI):
    cur.execute("""UPDATE vesseldetails SET updatedate = timestamp(0) WHERE mmsi = %(mmsi);""", {'mmsi':MMSI})
    conn.commit()
