import pymysql


class utilSql:
    conn_mysql = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password='root',
        database="baiduindex"
    )
    cursor_mysql = conn_mysql.cursor()

    def __init__(self):
        pass

    def selectWords(self):
        select_sql = "SELECT `keyword` FROM `keywords` GROUP BY `keyword`"
        self.cursor_mysql.execute(select_sql)
        results = self.cursor_mysql.fetchall()
        return results

    def createTableDemandChart(self):
        sql = '''
        create table if not exists demandChart(
            keyword varchar(100) not null,
            word varchar(100) not null,
            pv int not null,
            sim int not null,
            ratio int not null,
            start_date date not null,
            end_date date not null
        );
        '''
        self.cursor_mysql.execute(sql)

    def insertDemandChart(self, keyword, wordlist, start_date, end_date):
        sql = """
              insert into demandChart(keyword,word,pv,sim,ratio,start_date,end_date)
              values({},{},{},{},{},{},{})
              """.format(
            "'" + keyword + "'",
            "'" + wordlist['word'] + "'", wordlist['pv'],
            wordlist['ratio'],
            wordlist['sim'],
            "'" + start_date + "'",
            "'" + end_date + "'"
        )
        self.cursor_mysql.execute(sql)
        self.conn_mysql.commit()
        print('插入成功！')

    def cretaeTableRegionchart(self):
        sql = """
            create table if not exists regionchart(
            keyword varchar(100) not null,
            startdate date,
            enddate date,
            prov json not null,
            city json not null 
            );
        """
        self.cursor_mysql.execute(sql)

    def insertRegionchart(self, key, start_date, end_date, prov, city):
        sql = """insert into regionchart(keyword,startdate,enddate,prov,city)
                        values ({},{},{},'{}','{}');
                        """.format(
            '"' + key + '"', "'" + start_date + "'", "'" + end_date + "'",
            prov, city)
        self.cursor_mysql.execute(sql)
        self.conn_mysql.commit()
        print('插入成功！')

    def createTablePersonchartgender(self):
        self.cursor_mysql.execute("""
            create table if NOT EXISTS personchartgender(
            word varchar(100) not null ,
            sex varchar(10) not null ,
            tgi varchar(10) not null,
            rate varchar(10) not null
            );
            """)

    def createTablePersonchartage(self):
        self.cursor_mysql.execute("""
        create table if NOT EXISTS personchartage(
        word varchar(100) not null,
        age varchar(10) not null,
        tgi varchar(10) not null ,
        rate varchar(10) not null 
        );
        """)

    def insertePersonchartgender(self, key, gender):
        self.cursor_mysql.execute("""
                    insert into personchartgender() values('{}','{}','{}','{}'); 
                """.format(key, gender['desc'], gender['tgi'], gender['rate']))
        self.conn_mysql.commit()
        print('插入成功！')

    def insertePersonchartage(self, key, age):
        self.cursor_mysql.execute("""
                    insert into personchartage() values('{}','{}','{}','{}'); 
                        """.format(key, age['desc'], age['tgi'], age['rate']))
        self.conn_mysql.commit()
        print('插入成功！')

    def createTablePersonchartlike(self):
        self.cursor_mysql.execute("""
        create table if NOT EXISTS personchartlike(
        word varchar(100) NOT NULL,
        interest varchar(10) not null ,
        tgi varchar(10) not null,
        rate varchar(10) not null);
        """)

    def insertePersonchartlike(self, key, interest):
        self.cursor_mysql.execute("""
                    insert into personchartlike() values ('{}','{}','{}','{}')
                    """.format(key, interest['desc'], interest['tgi'], interest['rate']))
        self.conn_mysql.commit()
        print('插入成功！')
