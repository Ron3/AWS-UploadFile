#coding=utf-8
"""
Create On 2017/3/6

@author: Ron2
"""


from Crypto.Cipher import AES


class BPAES(object):
    """
    此模块用于加密和解密数据包.目前采用的加密算法是AES 128位加解密算法
    """

    AES_MODE = AES.MODE_CBC
    # AES_MODE = AES.MODE_ECB

    '''加密密key'''
    AES_KEY = "adgjmpbp**@!bpm@"

    # AES_KEY = "0123456789123456"

    @staticmethod
    def aes128_decrypt(requestData):
        """
        AES解密
        :param requestData:
        :return:
        """

        aes = AES.new(BPAES.AES_KEY, BPAES.AES_MODE)
        data = aes.decrypt(requestData)
        rawDataLength = len(data)
        paddingNum = ord(data[rawDataLength - 1])
        if paddingNum > 0 and paddingNum <= 16:
            data = data[0:(rawDataLength - paddingNum)]
        return data


    @staticmethod
    def aes128_encrypt(responseData):
        """
        加密
        :param responseData:
        :return:
        """
        size = len(responseData)
        diff = 16 - size % 16
        tmp = ""

        for i in range(diff):
            responseData += chr(diff)

        # for i in range(diff-1):
        #            tmp += '\r'
        #        responseData += tmp
        #        responseData += chr(diff)

        aes = AES.new(BPAES.AES_KEY, BPAES.AES_MODE)
        responseData = aes.encrypt(responseData)
        return responseData


if __name__ == "__main__":
    data = '''{"isGM": false, "mac": "40:6C:8F:59:31:EA", "tag": 100021, "type":15002}'''
    data = BPAES.aes128_encrypt(data)
    print BPAES.aes128_decrypt(data)


