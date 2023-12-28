# -*- coding: utf-8 -*-
import whois

# 동작 로깅용도
import logging
logger = logging.getLogger('django')

# URL 정보를 통해 서버 세부 정보 및 운영자 정보를 조회한다.
# input : 조회할 URL 주소 정보
# return : whois 조회 결과(domain_name, email, address, city, country)
def get(url):
    logger.info("[*] whois.get - START")
    
    result = []
    
    try:
        information = whois.whois(url)
        result.append(information.domain_name)
        result.append(information.emails)
        result.append(information.address)
        result.append(information.city)
        result.append(information.country)
        logger.info("[*] whois.get - FINISH")
        return result
        
    
    except Exception as e:
        logger.warning("[*] whois.get - ERROR : " + str(e))
        return None
        
    