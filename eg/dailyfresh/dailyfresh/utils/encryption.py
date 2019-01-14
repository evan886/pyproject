import hashlib

class Encrytion(object):

    def sha1(text):
        return hashlib.sha1(text.encode('utf-8')).hexdigest()



if __name__ == '__main__':
    print(Encrytion.sha1('aaskdjfh'))
