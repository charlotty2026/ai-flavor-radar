#!/usr/bin/env python3
"""
AI 味雷达 - 基础测试
运行: python3 tests/test_basic.py
"""

import sys
import os
import json
import subprocess

# 添加项目根目录到 path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from ai_flavor_radar import FlavorRadar, ScanResult


def test_rule_loading():
    """测试规则文件加载"""
    radar = FlavorRadar(mode="bid")
    assert len(radar.rules) > 0, "规则加载失败：规则列表为空"

    # 通用规则应该总是加载
    rule_ids = [r["id"] for r in radar.rules]
    assert "C01" in rule_ids, "通用规则 C01 未加载"
    assert "B01" in rule_ids, "投标规则 B01 未加载"

    radar_social = FlavorRadar(mode="social")
    social_ids = [r["id"] for r in radar_social.rules]
    assert "S01" in social_ids, "自媒体规则 S01 未加载"
    assert "B01" not in social_ids, "自媒体模式不应加载投标规则"

    print("✅ test_rule_loading 通过")


def test_detection():
    """测试基本检测功能"""
    radar = FlavorRadar(mode="bid")

    # 测试套话检测
    text = "众所周知，我们将为客户提供高效、专业、优质的全方位服务保障。"
    result = radar.scan(text)
    assert isinstance(result, ScanResult), "scan() 应返回 ScanResult"
    assert result.hit_count > 0, "检测失败：应命中多条规则"

    # 检查是否命中骈文
    hit_names = [h.rule_name for h in result.hits]
    assert any("骈文" in n or "套话" in n for n in hit_names), f"应检测到骈文或套话，实际命中: {hit_names}"

    print(f"✅ test_detection 通过 (命中 {result.hit_count} 条)")


def test_empty_text():
    """测试空文本"""
    radar = FlavorRadar(mode="bid")
    result = radar.scan("")
    assert result.hit_count == 0, "空文本不应有命中"
    assert result.score == 0, "空文本评分应为0"
    print("✅ test_empty_text 通过")


def test_clean_text():
    """测试干净文本（无AI味）"""
    radar = FlavorRadar(mode="bid")
    text = "本项目配置5名驻场人员，分两班次轮换，每班12小时。人员均持有相关岗位证书。"
    result = radar.scan(text)
    # 干净文本应该命中很少或零命中
    assert result.hit_count <= 1, f"干净文本命中过多: {result.hit_count} 条"
    print(f"✅ test_clean_text 通过 (命中 {result.hit_count} 条, 评分 {result.score})")


def test_scoring():
    """测试评分机制"""
    radar = FlavorRadar(mode="bid")

    # 重度AI味文本
    heavy_text = (
        "众所周知，我们将为客户提供高效、专业、优质的全方位服务保障。\n"
        "建立完善的管理机制，以科学为引领，以技术为支撑，以服务为保障。\n"
        "作为一个AI助手，我建议建立完善的考核机制。\n"
    )
    result = radar.scan(heavy_text)
    assert result.score > 30, f"重度AI味文本评分应>30，实际{result.score}"

    print(f"✅ test_scoring 通过 (重度文本评分: {result.score}/100, 命中: {result.hit_count} 条)")


def test_json_output():
    """测试JSON输出格式"""
    result = subprocess.run(
        [sys.executable, os.path.join(PROJECT_ROOT, "ai_flavor_radar.py"),
         os.path.join(PROJECT_ROOT, "examples", "sample_bid.txt"),
         "--mode", "bid", "--format", "json", "--no-color"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"脚本执行失败: {result.stderr}"

    data = json.loads(result.stdout)
    assert "score" in data, "JSON输出缺少score字段"
    assert "hits" in data, "JSON输出缺少hits字段"
    assert "file_path" in data, "JSON输出缺少file_path字段"
    assert "mode" in data, "JSON输出缺少mode字段"
    assert data["mode"] == "bid", f"mode应为bid，实际{data['mode']}"

    print(f"✅ test_json_output 通过 (评分: {data['score']}/100, 命中: {len(data['hits'])} 条)")


def test_markdown_output():
    """测试Markdown输出格式"""
    result = subprocess.run(
        [sys.executable, os.path.join(PROJECT_ROOT, "ai_flavor_radar.py"),
         os.path.join(PROJECT_ROOT, "examples", "sample_social.txt"),
         "--mode", "social", "--format", "markdown", "--no-color"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
    assert "# AI味雷达扫描报告" in result.stdout, "Markdown输出缺少标题"
    assert "AI味评分" in result.stdout, "Markdown输出缺少评分"

    print("✅ test_markdown_output 通过")


def test_stdin_input():
    """测试stdin输入"""
    result = subprocess.run(
        [sys.executable, os.path.join(PROJECT_ROOT, "ai_flavor_radar.py"),
         "--stdin", "--mode", "bid", "--format", "json", "--no-color"],
        input="众所周知，这是一个高效的方案。",
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["hit_count"] > 0, "stdin输入应检测到AI味"

    print(f"✅ test_stdin_input 通过 (命中: {data['hit_count']} 条)")


def test_no_duplicate_patterns():
    """测试规则文件无重复pattern"""
    rules_dir = os.path.join(PROJECT_ROOT, "rules")
    for fname in os.listdir(rules_dir):
        if not fname.endswith(".json") or fname == "whitelist.json":
            continue
        with open(os.path.join(rules_dir, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        for rule in data["rules"]:
            patterns = rule.get("patterns", [])
            if len(patterns) != len(set(patterns)):
                dupes = [p for p in patterns if patterns.count(p) > 1]
                assert False, f"{fname} 规则 {rule['id']} 有重复pattern: {set(dupes)}"
    print("✅ test_no_duplicate_patterns 通过")


def test_rule_structure():
    """测试规则文件结构完整性"""
    rules_dir = os.path.join(PROJECT_ROOT, "rules")
    required_fields = {"id", "name", "category", "severity", "suggestion"}
    valid_severities = {"fatal", "high", "medium", "low"}

    for fname in os.listdir(rules_dir):
        if not fname.endswith(".json") or fname == "whitelist.json":
            continue
        with open(os.path.join(rules_dir, fname), "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "rules" in data, f"{fname} 缺少 rules 键"
        for rule in data["rules"]:
            missing = required_fields - set(rule.keys())
            assert not missing, f"{fname} 规则 {rule.get('id','?')} 缺少字段: {missing}"
            assert rule["severity"] in valid_severities, \
                f"{fname} 规则 {rule['id']} severity 无效: {rule['severity']}"
            # 规则必须有 patterns 或 custom_check 至少一个
            has_patterns = "patterns" in rule and len(rule.get("patterns", [])) > 0
            has_custom = "custom_check" in rule and rule["custom_check"]
            assert has_patterns or has_custom, \
                f"{fname} 规则 {rule['id']} 既无 patterns 也无 custom_check"

    print("✅ test_rule_structure 通过")


def test_docx_output():
    """测试Word修订标记输出"""
    output_path = "/tmp/test_ai_radar_docx.docx"
    result = subprocess.run(
        [sys.executable, os.path.join(PROJECT_ROOT, "ai_flavor_radar.py"),
         os.path.join(PROJECT_ROOT, "examples", "sample_bid.txt"),
         "--mode", "bid", "--format", "docx", "-o", output_path],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
    assert os.path.exists(output_path), "docx文件未生成"
    
    # 验证docx内容
    from docx import Document
    doc = Document(output_path)
    xml_content = doc.element.xml
    assert 'w:del' in xml_content, "docx中缺少删除标记(w:del)"
    assert 'w:ins' in xml_content, "docx中缺少插入标记(w:ins)"
    
    # 清理
    os.remove(output_path)
    print("✅ test_docx_output 通过")


def run_all():
    """运行所有测试"""
    print("=" * 50)
    print("  AI 味雷达 - 基础测试套件")
    print("=" * 50)
    print()

    tests = [
        test_rule_loading,
        test_detection,
        test_empty_text,
        test_clean_text,
        test_scoring,
        test_json_output,
        test_markdown_output,
        test_stdin_input,
        test_no_duplicate_patterns,
        test_rule_structure,
        test_docx_output,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1

    print()
    print(f"结果: {passed} 通过, {failed} 失败, 共 {len(tests)} 项")

    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 全部通过！")


if __name__ == "__main__":
    run_all()
