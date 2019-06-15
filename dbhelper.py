import sqlite3
from jaraklokasi import jarak,bounding


class DBHelper:

	def __init__(self, dbname="ngaji.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname,check_same_thread=False)

	def setup(self):
		tblstmt = "CREATE TABLE IF NOT EXISTS ngaji ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, agenda text,pembicara text,materi text,lokasi text,hari text,tanggal text,waktu text,host text,lat text,lon text,owner text )"
		itemidx = "CREATE INDEX IF NOT EXISTS ngajiIndex ON ngaji (id ASC)" 
		ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON ngaji (owner ASC)"
		pointidx = "CREATE INDEX IF NOT EXISTS pointIndex ON ngaji (lat,lon)"
		self.conn.execute(tblstmt)
		self.conn.execute(itemidx)
		self.conn.execute(ownidx)
		self.conn.commit()

	def add_info(self,agd,ust,hal,loc,hr,tgl,jam,host,lat,lon,owner):
		stmt = "INSERT INTO ngaji VALUES(null,?,?,?,?,?,?,?,?,?,?,?)"
		args = (agd,ust,hal,loc,hr,tgl,jam,host,lat,lon,owner)
		try :
			self.conn.execute(stmt, args)
			self.conn.commit()
		except sqlite3.Error as er:
			print('er: ',er)

	def delete_info(self, id, owner):
		stmt = "DELETE FROM ngaji WHERE id = (?) AND owner = (?)"
		args = (id, owner )
		self.conn.execute(stmt, args)
		self.conn.commit()

	def get_info(self, owner):
		stmt = "SELECT agenda,pembicara,materi FROM ngaji WHERE owner = (?)"
		args = (owner, )
		return [x[0] for x in self.conn.execute(stmt, args)]

	def get_detail(self,id):
		stmt ="SELECT agenda,materi,pembicara,tanggal,waktu,lokasi,(lat||','||lon) as latlon,host FROM ngaji WHERE id = (?)"
		args = (id,)
		data = self.conn.execute(stmt,args)
		#print(data.description)
		res = {}
		colname = [d[0] for d in data.description]
		#print(data.fetchone())
		for i,r in enumerate(data.fetchone()):
			#print(i,r)
			res[colname[i]] = r
		#print(res)
		#result = [dict(zip(colname,r)) for r in data.fetchall()]
		return res

	def get_sepekan(self):
		stmt = "SELECT id,agenda,host FROM ngaji WHERE tanggal BETWEEN date('now','start of day') AND date('now','+7 days') ORDER BY tanggal ASC"
		data = self.conn.execute(stmt)
		all = data.fetchall()
		if not all:
			return None #"data tidak ditemukan"
		else : 
			return all

	def get_nearest(self,lokasi,rad):
		around = bounding(lokasi,rad)
		print(around)
		self.conn.create_function('jarak',4,jarak)
		stmt = ("select id,agenda,host,jarak(:slat,:slon,CAST(lat as real),CAST(lon as real)) as D from "
			"(SELECT id,agenda,host,lat,lon FROM ngaji "
			"WHERE lat BETWEEN :minlat AND :maxlat AND lon BETWEEN :minlon AND :maxlon "
			"AND tanggal BETWEEN date('now','start of day') AND date('now','+7 days')) as FirstCut"
			" WHERE jarak(:slat,:slon,CAST(lat as real),CAST(lon as real)) < :rad ORDER BY D")
		#.format(lokasi)) #,around[0],around[1],around[2],around[3],lokasi,rad))
		#my = "SELECT id,agenda,host,lat,lon from ngaji where lat between :minlat AND :maxlat AND lon between :minlon AND :maxlon" #.format(around[0],around[1],around[2],around[3])  
		par ={'slat':lokasi[0],'slon':lokasi[1],'rad':rad,'minlat':around[0],'maxlat':around[1],'minlon':around[3],'maxlon':around[2]}
		#print(par[0])
		#print(stmt)
		#test = "select agenda from ngaji order by (({}-lat)*({}-lat)) + (({}-lon)*({}-lon)) ASC".format(lokasi[0],lokasi[0],lokasi[1],lokasi[1])
		#print(test)
		sqlite3.enable_callback_tracebacks(True)
		data = self.conn.execute(stmt,par)

		all = data.fetchall()
		#print(all)
		if not all:
			return  None #"tidak ada lokasi terdekat"
		else :
			return all 
