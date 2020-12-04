import configparser
config = configparser.ConfigParser()
con_file = './config/att.cfg'
config.read(con_file)
network = config.sections()
print("network",network)