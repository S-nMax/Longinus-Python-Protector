# Longinus

import os
import base64
import zlib
import marshal
import types
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

CHUNK_SIZE = 500  # 每个属性链的最大比特数

# AES配置
AES_KEY_SIZE = 32  # AES-256
AES_IV_SIZE = 16   # AES块大小

# ---------- 反反汇编函数 ----------
def safe_insert_anti_disassembly(code_bytes):
    safe_opcodes = [0x09, 0x64, 0x53, 0x58, 0x5A]
    garbage = bytes([random.choice(safe_opcodes) for _ in range(random.randint(5, 10))])
    anti_code = b''
    for _ in range(random.randint(1, 2)):
        jump_target = random.randint(0, len(garbage) - 1)
        anti_code += bytes([0x71, jump_target & 0xFF, (jump_target >> 8) & 0xFF])
        anti_code += bytes([0x09])
    return code_bytes + anti_code + garbage

def encrypt_code(code_obj):
    """递归加密 code object，返回新对象"""
    new_consts = []
    for const in code_obj.co_consts:
        if isinstance(const, types.CodeType):
            new_consts.append(encrypt_code(const))
        else:
            new_consts.append(const)

    new_bytecode = safe_insert_anti_disassembly(code_obj.co_code)

    return types.CodeType(
        code_obj.co_argcount,
        code_obj.co_posonlyargcount if hasattr(code_obj, 'co_posonlyargcount') else 0,
        code_obj.co_kwonlyargcount,
        code_obj.co_nlocals,
        code_obj.co_stacksize,
        code_obj.co_flags,
        new_bytecode,
        tuple(new_consts),
        code_obj.co_names,
        code_obj.co_varnames,
        code_obj.co_filename,
        code_obj.co_name,
        code_obj.co_firstlineno,
        code_obj.co_lnotab,
        code_obj.co_freevars,
        code_obj.co_cellvars
    )
# ----------------------------------------------

def bytes_to_binary(data):
    """将字节串转换为8位二进制串"""
    return ''.join(format(b, '08b') for b in data)

def generate_random_word(length=None):
    """生成一个随机单词（大写字母串）"""
    if length is None:
        length = random.randint(3, 6)
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_underscore_string(min_len=1, max_len=5):
    """生成一个由下划线组成的字符串，长度随机"""
    length = random.randint(min_len, max_len)
    return '_' * length

def obfuscate_python_code(original_code, pool0=None, pool1=None, var_name='___', trigger='___'):
    """
    混淆 Python 代码
    :param original_code: 原始代码字符串
    :param pool0: 代表比特 0 的符号列表（每个元素必须是合法标识符）
    :param pool1: 代表比特 1 的符号列表
    :param var_name: 存放实例的变量名
    :param trigger: 触发执行的最终属性名
    """
    if pool0 is None:
        pool0 = [generate_random_word() for _ in range(random.randint(5, 10))]
    if pool1 is None:
        pool1 = [generate_random_word() for _ in range(random.randint(5, 10))]

    # 确保 var_name 和 trigger 不在池中
    all_pool_symbols = set(pool0) | set(pool1)
    while trigger in all_pool_symbols or trigger == var_name:
        trigger += '_'
    while var_name in all_pool_symbols or var_name == trigger:
        var_name += '_'

    print("正在使用AES加密原始代码...")
    
    # 生成AES密钥和IV
    key = os.urandom(AES_KEY_SIZE)  # 32字节的随机密钥
    iv = os.urandom(AES_IV_SIZE)    # 16字节的随机IV
    
    # AES-CBC加密
    cipher = AES.new(key, AES.MODE_CBC, iv)
    original_bytes = original_code.encode('utf-8')
    padded_bytes = pad(original_bytes, AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_bytes)
    
    # 只对加密后的数据进行二进制转换（不包含密钥和IV）
    binary = bytes_to_binary(encrypted_bytes)
    
    total_bits = len(binary)
    print(f"原始代码已加密，共 {total_bits} 比特 (AES-256)")

    pool0_str = repr(pool0)
    pool1_str = repr(pool1)

    # 将密钥和IV转换为可存储的格式
    key_b64 = base64.b64encode(key).decode('ascii')
    iv_b64 = base64.b64encode(iv).decode('ascii')

    Longinus_source = f'''try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    print('请先安装: pip install pycryptodome')
    raise SystemExit

import base64, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Longinus:
    def __init__(s):
        s.bits = ''
        s.encrypted = bytearray()
        s.key_b64 = '{key_b64}'
        s.iv_b64 = '{iv_b64}'
        s.pool0 = {pool0_str}
        s.pool1 = {pool1_str}
        s.set0 = set(s.pool0)
        s.set1 = set(s.pool1)
    def __getattr__(s, n):
        if n in s.set0:
            b = '0'
        elif n in s.set1:
            b = '1'
        elif n == '{trigger}':
            if s.bits:
                s.encrypted.append(int(s.bits.ljust(8, '0'), 2))
            
            all_bytes = bytes(s.encrypted)
            
            if len(all_bytes) % AES.block_size != 0:
                all_bytes = all_bytes[:len(all_bytes) - (len(all_bytes) % AES.block_size)]
            
            if not all_bytes:
                raise ValueError("没有接收到有效的加密数据")
            
            try:
                key = base64.b64decode(s.key_b64)
                iv = base64.b64decode(s.iv_b64)
            except Exception as e:
                raise ValueError(f"密钥/IV解码失败: {{e}}")
            
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted_padded = cipher.decrypt(all_bytes)
                decrypted = unpad(decrypted_padded, AES.block_size)
                
                try:
                    code_str = decrypted.decode('utf-8')
                except UnicodeDecodeError:
                    raise ValueError("解密后的数据无法用utf-8解码")
                
            except Exception as e:
                raise ValueError(f"AES解密失败: {{e}}")
            
            exec(code_str, globals())
            return s
        else:
            return s
        s.bits += b
        if len(s.bits) == 8:
            s.encrypted.append(int(s.bits, 2))
            s.bits = ''
        return s
'''

    print("正在编译 Longinus 类并应用反反汇编...")
    Longinus_code_obj = compile(Longinus_source, '<Longinus>', 'exec')
    protected_Longinus = encrypt_code(Longinus_code_obj)

    Longinus_marshaled = marshal.dumps(protected_Longinus)
    Longinus_compressed = zlib.compress(Longinus_marshaled)
    Longinus_b64 = base64.b64encode(Longinus_compressed).decode('ascii')
    Longinus_bytes_literal = f"b'{Longinus_b64}'"

    print("正在生成属性链...")
    chunks = []
    start = 0
    chunk_index = 1
    total_chunks = (total_bits + CHUNK_SIZE - 1) // CHUNK_SIZE
    while start < total_bits:
        end = min(start + CHUNK_SIZE, total_bits)
        chunk = binary[start:end]
        chain_parts = []
        for bit in chunk:
            if bit == '0':
                sym = random.choice(pool0)
            else:
                sym = random.choice(pool1)
            chain_parts.append(f'.{sym}')
        chain = ''.join(chain_parts)
        chunks.append(chain)
        start = end
        print(f"  已处理 chunk {chunk_index}/{total_chunks}")
        chunk_index += 1

    assignments = [f"{var_name} = {var_name}{chain}" for chain in chunks]
    assignments_line = "; ".join(assignments) + f"; {var_name}.{trigger}"

    lines = [
        "import base64,zlib,marshal,hashlib",
        f"exec(marshal.loads(zlib.decompress(base64.b64decode({Longinus_bytes_literal}))), globals()); {var_name} = Longinus()",
        assignments_line
    ]
    return "\n".join(lines)

def main():
    file_path = input("请输入要混淆的Python文件路径: ").strip()
    if not os.path.isfile(file_path):
        print("文件不存在，请检查路径。")
        return

    print("\n请选择混淆模式：")
    print("1. 完全随机字母（变量名、触发属性、符号池全随机，视觉上像无意义单词）")
    print("2. 点下划线风格（变量名/触发属性为下划线组合，0用短下划线，1用长下划线）")
    print("3. 手动自定义")
    mode = input("请输入模式编号 (1/2/3): ").strip()

    pool0 = pool1 = None
    var_name = '___'
    trigger = '___'

    if mode == '1':
        var_name = generate_random_word(4)
        trigger = generate_random_word(4)
        pool0 = [generate_random_word() for _ in range(random.randint(5, 10))]
        pool1 = [generate_random_word() for _ in range(random.randint(5, 10))]
        all_symbols = set(pool0) | set(pool1)
        while var_name in all_symbols or var_name == trigger:
            var_name = generate_random_word(4)
        while trigger in all_symbols or trigger == var_name:
            trigger = generate_random_word(4)
        print(f"自动生成：变量名={var_name}, 触发属性={trigger}")
    elif mode == '2':
        var_name = generate_underscore_string(2, 5)
        trigger = generate_underscore_string(2, 5)
        # 生成池时避免与 var_name/trigger 相同
        def gen_pool0():
            while True:
                s = generate_underscore_string(1, 3)
                if s != var_name and s != trigger:
                    return s
        def gen_pool1():
            while True:
                s = generate_underscore_string(4, 6)
                if s != var_name and s != trigger:
                    return s
        pool0 = [gen_pool0() for _ in range(random.randint(5, 10))]
        pool1 = [gen_pool1() for _ in range(random.randint(5, 10))]
        pool0 = list(set(pool0))
        pool1 = list(set(pool1))
        while len(pool0) < 3:
            pool0.append(gen_pool0())
        while len(pool1) < 3:
            pool1.append(gen_pool1())
        print(f"自动生成：变量名={var_name}, 触发属性={trigger}")
        print(f"符号池0示例：{pool0[:3]}... 共{len(pool0)}个")
        print(f"符号池1示例：{pool1[:3]}... 共{len(pool1)}个")
    elif mode == '3':
        var_name = input("请输入变量名（默认 '___'）: ").strip() or '___'
        trigger = input("请输入触发属性名（默认 '___'）: ").strip() or '___'
        sym0_input = input("请输入代表0的符号列表（逗号分隔，如 A,B,C）: ").strip()
        sym1_input = input("请输入代表1的符号列表（逗号分隔，如 X,Y,Z）: ").strip()
        if sym0_input:
            pool0 = [s.strip() for s in sym0_input.split(',') if s.strip()]
        if sym1_input:
            pool1 = [s.strip() for s in sym1_input.split(',') if s.strip()]
        if pool0 is None:
            pool0 = [generate_random_word() for _ in range(random.randint(5, 10))]
        if pool1 is None:
            pool1 = [generate_random_word() for _ in range(random.randint(5, 10))]
        all_symbols = set(pool0) | set(pool1)
        while var_name in all_symbols or var_name == trigger:
            var_name += '_'
        while trigger in all_symbols or trigger == var_name:
            trigger += '_'
    else:
        print("无效模式，退出。")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        original = f.read()

    print("开始混淆...")
    obfuscated = obfuscate_python_code(original, pool0, pool1, var_name, trigger)

    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_obf{ext}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(obfuscated)

    print(f"混淆完成！输出文件：{output_path}")

if __name__ == "__main__":
    main()
