class Loggable:
    def __init__(self) -> None:
        self.title = ''

    def log(self):
        print(f'Logged from {self.title}')


class Connection:
    def __init__(self) -> None:
        self.server = ''

    def connect(self):
        print(f'Connecting to Database on {self.server}')


def framework(item):
    # Perform the connection
    if isinstance(item, Connection):
        item.connect()

    if isinstance(item, Loggable):
        item.log()


con = Connection()
con.server = 'Little Server'
log = Loggable()
log.title = 'Cachula'

framework(con)
framework(log)


class SqlDatabase(Connection, Loggable):
    def __init__(self, title, server) -> None:
        super().__init__()
        self.title = title
        self.server = server


sql_database = SqlDatabase('Sql Connection Demo', 'Some_Server')
framework(sql_database)
