# -*- coding: utf-8 -*-

def test():
    rxcount = 0
    txcount = 0
    testcount = 0
    index = 0
    num = 0
    with open('ttt.log', 'r') as f:
        done = 0
        while not done:
            line = f.readline()
            num += 1
            if line:
                rxcount = 0
                txcount = 0
                while line != '\n' and line != '':
                    if line.startswith('slb.rx.'):
                        rxcount += 1
                    if line.startswith('slb.tx'):
                        txcount += 1
                    line = f.readline()
                    num += 1
                if rxcount != txcount:
                    print num, rxcount, txcount
            else:
                done = 1


if __name__ == '__main__':
    test()