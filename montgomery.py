#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from math import log2


def expand(n: int) -> list:
    """
    数字转数组，进制为r
    """
    result = []
    while n >= r:
        result.append(n % r)
        n //= r
    result.append(n)
    return result


def join(l: list) -> int:
    """
    数组转数字，进制为r
    """
    result = 0
    for index, n in enumerate(l):
        result += r ** index * n
    return result


def ext_euclid(a: int, b: int) -> (int, int, int):
    """
    扩展欧几里得算法
    给予二整数 a 与 b, 必存在有整数 x 与 y 使得 ax + by = gcd(a,b)
    q 为最大公约数
    """
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = ext_euclid(b, a % b)
        # q = gcd(a, b) = gcd(b, a%b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


def mod_reverse(a: int, p: int) -> int:
    """
    求a的逆元x，使得 ax = 1 (mod p)
    """
    #
    x, y, q = ext_euclid(a, p)
    if q == 1:
        return (x % p + p) % p
    print("mod_reverse fuck")
    return -1


def mont_format(x: list) -> list:
    """
    x => x*R mod P
    """
    return mont_mul_mod(x, expand(RR))  # 等价于 expand(join(x) * join(R) % join(P))


def mont_mul_mod(x: list, y: list) -> list:
    """
    x * y * R^-1 mod P
    x、y 的长度应和R保持一致
    """
    D = 0
    D0 = 0
    Y0 = y[0]
    Y = join(y)
    for Xi in x:
        q = (D0 + Y0*Xi) * W
        q = q % r
        D += Xi * Y + q * join(P)
        D //= r
        D0 = expand(D)[0]
    if D >= join(P):
        D -= join(P)
    return expand(D)


def reduce2(T: int) -> int:
    """
    T -> T * R^-1 mod P
    用于验证mont_reduce()结果是否正确
    """
    R_1 = mod_reverse(join(R), join(P))
    return T * R_1 % join(P)


def mont_reduce(T: list) -> list:
    """
    T -> T * R^-1 mod P
    """
    t = join(T)
    m = int(log2(join(R)))                                # 256
    q = ((t & (join(R)-1)) * P_) & (join(R)-1)      # q = (T%R)*P_ % R
    a = (t + q * join(P)) >> m                      # a = (T+q*P) // R
    if a > join(P):
        a -= join(P)
    return expand(a)


r = 2**64       # 进制，every element in list is a uint64
R = expand(2**256)       # 256位
P = expand(0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001)    # 有限域的阶

RR = join(R) * join(R) % join(P)        # R^2 mod P, 使用常规方法提前计算好

# 由 R * R^-1 - P * P' = 1
# 得到 R * R^-1 = 1 mod P 和 P * P' = -1 mod R
# 所以，R^-1 称为R的模P逆，P'称为P的模R负逆
# 其他一些后面会用到的常量，提前计算好
R_1 = mod_reverse(join(R), join(P))     # R^-1
P_ = (join(R) * R_1 - 1) // join(P)     # P'
P0_1 = mod_reverse(P[0], r)             # P0^-1
W = -P0_1 % r                           # W = r - P0_1


def field_mul(A: list, B: list) -> list:
    """
    A * B mod P
    """
    AR = mont_format(A)
    BR = mont_format(B)
    ABR = mont_mul_mod(AR, BR)
    AB = mont_reduce(ABR)
    return AB


if __name__ == '__main__':
    print("RR is", hex(RR))
    print("P' is", hex(P_))
    print("P0^-1 is", hex(P0_1))
    print("W is", hex(W))

    # en example of calculating A^5 mod P
    A = expand(0x5abfcc164e7baae2ef0c3e3f77b3e0d48d76f90f2d3bd2e206b6bbde7340966f)
    A2 = field_mul(A, A)
    A4 = field_mul(A2, A2)
    A5 = field_mul(A, A4)
    print("A^5 mod P is", hex(join(A5)))

