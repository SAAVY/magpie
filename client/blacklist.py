from flask import current_app
from netaddr import IPNetwork, IPAddress
from netaddr.core import AddrFormatError


bl_request_ip = []  # array of tuples (network mask, port)
bl_website_ip = []  # array of tuples (network mask, port)


def build_inc_request_blacklist(logger):
    with open("config/blacklist_inc_request_ip.txt") as f:
        for line in f:
            network_address = line.strip()
            ip, separator, port = network_address.rpartition(':')
            if separator:
                logger.error("check blacklist_inc_request_ip.txt: cannot specify port number in network mask")
                continue
            try:
                IPNetwork(network_address)
                bl_request_ip.append((network_address, ''))
            except AddrFormatError as e:
                logger.error("Format error. check blacklist_inc_request_ip.txt: %s" % str(e))


def build_website_blacklist(logger):
    with open("config/blacklist_website_ip.txt") as f:
        for line in f:
            network_address = line.strip()
            ip, separator, port = network_address.rpartition(':')
            if not separator:
                address = (network_address, '')
            else:
                address = (ip, port)
                if not port:
                    logger.error("check blacklist_website_ip.txt: must specify port number after ':' in ip")
                    continue
            try:
                IPNetwork(address[0])
                bl_website_ip.append(address)
            except AddrFormatError as e:
                logger.error("Format error. check blacklist_website_ip.txt: %s" % str(e))


def is_inc_request_blacklisted(ip_address):
    logger = current_app.logger
    logger.debug("FUNC: is_inc_request_blacklisted ip_address: %s" % ip_address)
    for network, _ in bl_request_ip:
        try:
            if IPAddress(ip_address) in IPNetwork(network):
                return True
        except Exception as e:
            logger.exception("FUNC: is_inc_request_blacklisted Exception: %s" % str(e))
    return False


def is_website_blacklisted(website_ip, website_port):
    logger = current_app.logger
    logger.debug("FUNC: is_website_blacklisted ip_address: %s port: %s" % (website_ip, website_port))
    for network_mask, port in bl_website_ip:
        try:
            if IPAddress(website_ip) in IPNetwork(network_mask):
                if port and website_port == port:
                    return True
                elif port:
                    return False
                return True
        except Exception as e:
            logger.exception("FUNC: is_website_blacklisted Exception: %s" % str(e))
    return False
