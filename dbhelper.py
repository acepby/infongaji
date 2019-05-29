import sqlite3


class DBHelper:

	def __init__(self, dbname="ngaji.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname,check_same_thread=False)

	def setup(self):
		tblstmt = "CREATE TABLE IF NOT EXISTS ngaji ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, agenda text,pembicara text,materi text,lokasi text,hari text,tanggal text,waktu text,host text,lat text,lon text,owner text )"
		itemidx = "CREATE INDEX IF NOT EXISTS ngajiIndex ON ngaji (id ASC)" 
		ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON ngaji (owner ASC)"
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
		stmt = "SELECT id,agenda,host FROM ngaji WHERE tanggal NOT NULL  AND (strftime('%W',tanggal)=strftime('%W','now'))"
		data = self.conn.execute(stmt)
		all = data.fetchall()
		if not all:
			print("data tidak ditemukan")
		else : 
			return all
