import rmapy.const

# Pulled from 'https://github.com/subutux/rmapy/pull/35'
# Thanks jwoglom
rmapy.const.AUTH_BASE_URL = "https://webapp-prod.cloud.remarkable.engineering"
rmapy.const.BASE_URL = "https://internal.cloud.remarkable.com"
rmapy.const.DEVICE_TOKEN_URL = rmapy.const.AUTH_BASE_URL + "/token/json/2/device/new"
rmapy.const.USER_TOKEN_URL = rmapy.const.AUTH_BASE_URL + "/token/json/2/user/new"