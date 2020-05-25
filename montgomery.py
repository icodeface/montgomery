#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from math import log2


def expand(n: int) -> list:
    result = []
    while n >= r:
        result.append(n % r)
        n //= r
    result.append(n)
    return result


def join(l: list) -> int:
    result = 0
    for index, n in enumerate(l):
        result += r ** index * n
    return result


def ext_euclid(a, b):
    # 扩展欧几里得算法
    # 给予二整数 a 与 b, 必存在有整数 x 与 y 使得 ax + by = gcd(a,b)
    # q 为最大公约数
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = ext_euclid(b, a % b)
        # q = gcd(a, b) = gcd(b, a%b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


def mod_reverse(a: int, p: int) -> int:
    # 求a的逆元x，使得 ax = 1(mod p)
    x, y, q = ext_euclid(a, p)
    if q == 1:
        return (x % p + p) % p
    print(f"fuck, 没找到 {a} 的逆元")
    return -1


def mont_format(x: list) -> list:
    # x => x*R mod P
    RR = join(R) * join(R) % join(P)    # R是常量，R^2 mod P 可提前计算
    return mont_mul_mod(x, expand(RR))
    # return expand(join(x) * join(R) % join(P))


def mont_mul_mod(x: list, y: list) -> list:
    # x * y * R^-1 mod P
    # x的长度应和R保持一致，y可以不定长
    D = 0
    D0 = 0

    Y0 = y[0]
    P0_1 = mod_reverse(P[0], r)  # P0^-1
    W = -P0_1 % r  # W_u64 = r - P0_1

    print(f"Y0: {hex(Y0)}\nP0^-1: {hex(P0_1)}")

    Y = join(y)
    for Xi in x:
        q = (D0 + Y0*Xi) * W
        q = q % r
        D += Xi * Y + q * join(P)
        D //= r
        print(f"q is {hex(q)}\nD is {hex(D)}")
        D0 = expand(D)[0]
    if D >= join(P):
        D -= join(P)
    return expand(D)


def reduce2(T: int) -> int:
    # T * R^-1 mod P
    R_1 = mod_reverse(join(R), join(P))  # R^-1 可预先计算好
    return T * R_1 % join(P)


def mont_reduce(T: list) -> list:
    t = join(T)
    R_1 = mod_reverse(join(R), join(P))
    P_ = (join(R) * R_1 - 1) // join(P)     # P' 可预先计算好
    print("P' is", hex(P_))
    m = (len(R) - 1) * int(log2(r))  # 256

    q = ((t & (join(R)-1)) * P_) & (join(R)-1)    # q = (T%R)*P_ % R
    a = (t + q * join(P)) >> m                    # a = (T+q*P) // R
    print(f"a is {hex(a)}, P is {hex(join(P))}")
    if a > join(P):
        a -= join(P)
    return expand(a)


r = 2**64  # uint64
R = expand(2**256)
P = expand(0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001)
A = expand(0x5abfcc164e7baae2ef0c3e3f77b3e0d48d76f90f2d3bd2e206b6bbde7340966f)


# 由 R * R^-1 - P * P' = 1
# 得到 R * R^-1 = 1 mod P 和 P * P' = -1 mod R
# 所以，R^-1 称为R的模P逆，P'称为P的模R负逆

def field_mul(a: list, b: list):
    AR = mont_format(a)
    BR = mont_format(b)
    ABR = mont_mul_mod(AR, BR)
    AB = mont_reduce(ABR)
    return AB


if __name__ == '__main__':
    A2 = field_mul(A, A)
    A4 = field_mul(A2, A2)
    A5 = field_mul(A, A4)
    print("A^5 mod P is", hex(join(A5)))

