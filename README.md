Longinus Python Code Obfuscator / Longinus Python代码混淆器

[AGPL-3.0 License] © 2026

"English" (#english) | "中文" (#中文)

English

Overview

Longinus is an advanced Python code protection tool that transforms readable Python scripts into heavily obfuscated versions. It employs multiple security layers including AES-256 encryption, bytecode manipulation, and attribute-based encoding to prevent reverse engineering and unauthorized analysis.

Key Features

- Multi-layer Encryption: AES-256 CBC encryption for source code protection
- Binary Encoding: Converts encrypted data to binary and encodes as attribute access chains
- Anti-Disassembly Protection: Bytecode manipulation to hinder static analysis
- Configurable Obfuscation: Multiple obfuscation modes with customizable symbols
- Chunked Processing: Handles large codebases by processing in manageable segments
- Self-contained Execution: Generates standalone obfuscated files

Installation

# Required dependencies
pip install pycryptodome

Usage

python longinus.py

1. Enter the path to your Python file
2. Choose obfuscation mode:
   - Mode 1: Random letters (variables, triggers, and symbol pools as random words)
   - Mode 2: Underscore style (variables/triggers as underscore combinations, 0=short underscores, 1=long underscores)
   - Mode 3: Manual customization
3. Output file: 
"{original_filename}_obf.py"

Obfuscation Modes

Mode 1: Random Letter Mode

- Variable names, trigger attributes, and symbol pools as random uppercase words
- Example: 
"VAR1.A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z._____"

Mode 2: Underscore Style

- Variables/triggers as underscore combinations (
"_", 
"__", 
"___")
- 0-bit: Short underscores (1-3 underscores)
- 1-bit: Long underscores (4-6 underscores)
- Example: 
"___._.___.__._____.__.__._____.___.___._____.____"

Mode 3: Custom Mode

- Manually specify variable names, trigger attributes, and symbol pools
- Full control over all obfuscation parameters

Technical Architecture

1. Encryption Layer

# AES-256 CBC encryption
key = os.urandom(32)  # 256-bit key
iv = os.urandom(16)   # 128-bit IV
cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted = cipher.encrypt(pad(source_code))

2. Binary Encoding

- Encrypted bytes → binary string (8-bit chunks)
- Binary bits → attribute accesses (0=pool0, 1=pool1)
- Example: Binary 
""01001000"" → 
".SYMBOL0.SYMBOL1.SYMBOL0.SYMBOL0.SYMBOL1..."

3. Execution Mechanism

# Obfuscated code structure
1. Decode/load Longinus class (base64+zlib+marshal)
2. Instantiate: var = Longinus()
3. Execute attribute chain: var.SYM0.SYM1.SYM0.SYM1.TRIGGER
4. Trigger reconstructs binary → decrypts → executes

4. Anti-Analysis Features

- Safe opcode insertion in bytecode
- Code object recursion protection
- Marshaling/compression/encoding chain

Security Features

- Encryption: AES-256 CBC with random IV
- Encoding: Binary conversion with custom symbol mapping
- Obfuscation: Variable name randomization, attribute chain fragmentation
- Anti-Debug: Anti-disassembly bytecode manipulation
- Data Hiding: Keys stored in base64 within the payload

Example

Original Code:

print("Hello, World!")

Obfuscated (simplified):

import base64,zlib,marshal,hashlib
exec(marshal.loads(zlib.decompress(base64.b64decode(b'eNrt...'))), globals()); ___ = Longinus()
___ = ___.A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z.___

Limitations

- Requires 
"pycryptodome" at runtime
- Increases code size significantly
- May impact performance on large codebases
- Not immune to determined reverse engineering

Development

# Project Structure
longinus.py          # Main obfuscator
example.py           # Example target code
example_obf.py       # Obfuscated output

License

AGPL-3.0 - See "LICENSE" (LICENSE) for details.

中文

概述

Longinus 是一个高级的Python代码保护工具，可将可读的Python脚本转换为高度混淆的版本。它采用多层安全防护，包括AES-256加密、字节码操作和基于属性的编码，以防止逆向工程和未经授权的分析。

主要特性

- 多层加密：AES-256 CBC加密保护源代码
- 二进制编码：将加密数据转换为二进制并通过属性访问链编码
- 反反汇编保护：字节码操作阻碍静态分析
- 可配置混淆：多种混淆模式，支持自定义符号
- 分块处理：通过分段处理支持大型代码库
- 自包含执行：生成独立的混淆文件

安装

# 必需依赖
pip install pycryptodome

使用方法

python longinus.py

1. 输入Python文件路径
2. 选择混淆模式：
   - 模式1：随机字母（变量、触发器和符号池均为随机单词）
   - 模式2：下划线风格（变量/触发器这下划线组合，0=短下划线，1=长下划线）
   - 模式3：手动自定义
3. 输出文件：
"{原文件名}_obf.py"

混淆模式

模式1：随机字母模式

- 变量名、触发器属性和符号池均为随机大写单词
- 示例：
"VAR1.A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z._____"

模式2：下划线风格

- 变量/触发器为下划线组合（
"_"、
"__"、
"___"）
- 0比特：短下划线（1-3个下划线）
- 1比特：长下划线（4-6个下划线）
- 示例：
"___._.___.__._____.__.__._____.___.___._____.____"

模式3：自定义模式

- 手动指定变量名、触发器属性和符号池
- 完全控制所有混淆参数

技术架构

1. 加密层

# AES-256 CBC加密
key = os.urandom(32)  # 256位密钥
iv = os.urandom(16)   # 128位初始向量
cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted = cipher.encrypt(pad(源代码))

2. 二进制编码

- 加密字节 → 二进制字符串（8位一组）
- 二进制位 → 属性访问（0=pool0，1=pool1）
- 示例：二进制
""01001000"" → 
".符号0.符号1.符号0.符号0.符号1..."

3. 执行机制

# 混淆代码结构
1. 解码/加载Longinus类（base64+zlib+marshal）
2. 实例化：变量 = Longinus()
3. 执行属性链：变量.符号0.符号1.符号0.符号1.触发器
4. 触发器重建二进制 → 解密 → 执行

4. 反分析特性

- 字节码中插入安全操作码
- 代码对象递归保护
- 序列化/压缩/编码链

安全特性

- 加密：AES-256 CBC带随机IV
- 编码：自定义符号映射的二进制转换
- 混淆：变量名随机化，属性链分段
- 反调试：反反汇编字节码操作
- 数据隐藏：密钥以base64格式存储在载荷中

示例

原始代码：

print("Hello, World!")

混淆后（简化版）：

import base64,zlib,marshal,hashlib
exec(marshal.loads(zlib.decompress(base64.b64decode(b'eNrt...'))), globals()); ___ = Longinus()
___ = ___.A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.W.X.Y.Z.___

限制

- 运行时需要
"pycryptodome"
- 显著增加代码大小
- 对大型代码库可能影响性能
- 无法完全阻止有决心的逆向工程

开发

# 项目结构
longinus.py          # 主混淆器
example.py           # 示例目标代码
example_obf.py       # 混淆输出

许可证

AGPL-3.0 - 详见 "LICENSE" (LICENSE) 文件。

注意：Longinus旨在提供代码保护，但无法保证绝对安全。请根据安全需求评估使用。
