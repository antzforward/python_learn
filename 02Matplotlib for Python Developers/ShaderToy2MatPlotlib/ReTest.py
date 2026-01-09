import re

import packaging
from packaging.version import Version

# pip 自己就很强啊 别这么搞了
package_parse_rex = re.compile(r"^\s*([a-zA-Z0-9_\-\.]+)\s*([<>!=~]+)?\s*([\w\.\*\-]+)?\s*$")

def parse_package_spec(spec_str):
    global  package_parse_rex
    """
    解析包规范字符串，返回包名、比较运算符和版本号
    格式示例:
        "package-name" -> ("package-name", "", "")
        "package-name>=1.2.3" -> ("package-name", ">=", "1.2.3")
        "package-name == 4.5.6" -> ("package-name", "==", "4.5.6")
    """
    # 使用正则表达式捕获包名、运算符和版本号
    match = re.match(package_parse_rex, spec_str)

    if not match:
        raise ValueError(f"Invalid package spec format: {spec_str}")

    package_name = match.group(1).strip()
    operator = (match.group(2) or "").strip()
    version = (match.group(3) or "").strip()

    return package_name, operator, version

# 使用示例
examples = [
    "package-name",
    "package-name>=1.2.3",
    "another_package == 4.5.6",
    "some.package ~= 7.8.9"
]

def _op_ver_check(op, ver, pre_op, pre_ver) -> tuple(bool, bool):
    # 设置完全
    if op == pre_op and ver == pre_ver:
        return pre_op, pre_ver
    # 不做任何变化
    if not ver:
        return pre_op, pre_ver

    # 如果没有安装版本，需要安装
    if not pre_ver:
        return op, ver

    # 版本比较逻辑
    installed = packaging.version.parse(pre_ver)
    required = packaging.version.parse(ver)

    # 版本相同，符号可能有不同，共点情况
    if installed == required:
        if (equal := '=') and equal in op and equal in pre_op:
            return '==', ver
        else:
            #这里可能有冲突，没有共同点，抛出异常信息
            raise ValueError(f"no version is match {op} {ver} with {pre_op} {pre_ver}")
    else: #版本不同，先确定线段的端点
        smaller,larger = (min(required,installed),max(required,installed))
        if op == pre_op:
            if (g := '>') and g in op and g in pre_op:
                return '>=',larger
            elif (l := '<') and l in op and l in pre_op:
                return '<=',smaller
            else:
                if '<' in op:
                    larger = min( ver, larger)
                if '>' in op:

            return installed != required
        elif op == ">=":
            return installed < required
        elif op == "<=":
            return installed > required
        elif op == ">":
            return installed <= required
        elif op == "<":
            return installed >= required
        elif op == "!=":
            return installed == required
        elif op == "~=":  # 兼容版本
            next_minor = required._version.release[:1] + (required._version.release[1] + 1,)
            next_minor_ver = packaging.version.Version(".".join(map(str, next_minor)))
            return not (installed >= required and installed < next_minor_ver)

    return True  # 未知操作符默认重新安装

for spec in examples:
    name, op, ver = parse_package_spec(spec)
    print(f"{spec!r:30} => Name: {name}, Operator: {op}, Version: {ver}")