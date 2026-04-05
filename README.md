# Longinus 🛡️  
*Advanced Python Code Obfuscator & Protector*

[中文](#chinese) | [English](#english)

---

<a name="english"></a>
## English

### Overview
**Longinus** is a Python code obfuscation and protection tool designed to make reverse engineering extremely difficult.  
It converts your Python source code into an **AES-256 encrypted bytecode**, reconstructs it using **attribute chaining**, and embeds it into a self-decrypting runtime loader.

The final output looks like meaningless attribute access chains, making static analysis and disassembly very hard.

### Key Features
- ✅ AES-256 CBC encryption for payload
- ✅ Attribute-chain based binary reconstruction
- ✅ Anti-disassembly bytecode manipulation
- ✅ Recursive `marshal` + `zlib` + `base64` protection
- ✅ Multiple obfuscation modes (random words / underscore style / custom)
- ✅ Trigger-based dynamic execution

### How It Works (Simplified)
1. Original Python code → UTF-8 bytes
2. AES-256 CBC encryption
3. Encrypted bytes → binary stream
4. Binary bits mapped to attribute chains (`pool0` = 0, `pool1` = 1)
5. Chains trigger `__getattr__` to rebuild encrypted data
6. On trigger: decrypt → decompress → execute via `exec`

### Usage
```bash
pip install pycryptodome
python longinus.py
```

Follow the prompts:
- Enter the path to the Python file you want to protect
- Choose obfuscation mode
- Get the obfuscated output file

### Example Output Structure
```python
import base64,zlib,marshal,hashlib
exec(marshal.loads(zlib.decompress(base64.b64decode(...))), globals()); ___ = Longinus()
___.ABCD.XYZQ.MNOP.___
```

### Warning
⚠️ This tool is intended for **legitimate code protection**.  
Do not use it to hide malicious software.

---

<a name="chinese"></a>
## chinese

### 项目简介
**Longinus** 是一个高级 Python 代码混淆与保护工具，旨在极大提高逆向工程的难度。  
它通过将 Python 源码进行 **AES-256 加密**，并以 **属性链（attribute chain）** 的形式重构执行流程，最终生成一个几乎不可读、难以静态分析的 Python 脚本。

### 核心特性
- ✅ 使用 AES-256 CBC 加密核心代码
- ✅ 基于属性访问链的比特流还原机制
- ✅ 反反汇编（Anti-disassembly）字节码注入
- ✅ 多层保护：`marshal` + `zlib` + `base64`
- ✅ 三种混淆模式：
  - 随机单词模式
  - 下划线风格模式
  - 手动自定义模式
- ✅ 触发式动态执行

### 工作原理（简化版）
1. 原始 Python 代码 → UTF-8 字节
2. AES-256 CBC 加密
3. 加密结果转为二进制流
4. 0/1 分别映射为两个符号池中的属性名
5. 利用 `__getattr__` 累积比特并还原密文
6. 触发属性执行：解密 → 解压 → `exec` 执行

### 使用方法
```bash
pip install pycryptodome
python longinus.py
```

按提示操作：
- 输入需要保护的 Python 文件路径
- 选择混淆模式
- 程序将生成混淆后的文件

### 示例结构
```python
import base64,zlib,marshal,hashlib
exec(marshal.loads(zlib.decompress(base64.b64decode(...))), globals()); xyz = Longinus()
xyz.KLMN.QRST.UVWX.___
```

### 注意事项
⚠️ 本工具仅供 **合法的代码保护与授权分发** 使用，  
请勿用于恶意软件或违反法律法规的场景。

---

## License
GNU AFFERO GENERAL PUBLIC LICENSE
