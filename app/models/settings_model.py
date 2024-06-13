settings_keys = [
    "MONITOR",
    "MONITOR_FOLDERS",
    "SYSTEM_HARDENING",
    "SSH_DEFAULT_PORT_CHECK",
    "EXCLUDE",
    "HONEYPOT_BAN",
    "WHITELIST_IP",
    "TCPPORTS",
    "UDPPORTS",
    "HONEYPOT_AUTOACCEPT",
    "SSH_BRUTE_MONITOR",
    "SSH_BRUTE_ATTEMPTS",
    "FTP_BRUTE_MONITOR",
    "FTP_BRUTE_ATTEMPTS",
    "ANTI_DOS",
    "ANTI_DOS_PORTS"
]

settings_defaults = {
    'MONITOR': True,
    'MONITOR_FOLDERS': '/var/www,/etc/', 
    'SYSTEM_HARDENING': True, 
    'SSH_DEFAULT_PORT_CHECK': True, 
    'EXCLUDE': '',
    'HONEYPOT_BAN': True, 
    'WHITELIST_IP': '127.0.0.1,localhost', 
    'TCPPORTS': '22,1433,8080,21,5060,5061,5900,25,53,110,1723,1337,10000,5800,44443,16993', 
    'UDPPORTS': '123,53,5060,5061,3478', 
    'HONEYPOT_AUTOACCEPT': True, 
    'SSH_BRUTE_MONITOR': True, 
    'SSH_BRUTE_ATTEMPTS': '4', 
    'FTP_BRUTE_MONITOR': True, 
    'FTP_BRUTE_ATTEMPTS': '4', 
    'ANTI_DOS': True, 
    'ANTI_DOS_PORTS': '80,443'
}