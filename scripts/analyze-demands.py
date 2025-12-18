#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
印度骑行拍摄诉求数据分析脚本

功能：
1. 加载和分析调研数据
2. 生成统计报告
3. 识别关键洞察
4. 导出分析结果

作者：印度骑行拍摄诉求分析项目组
日期：2025-12-18
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter


class DemandAnalyzer:
    """需求分析器"""
    
    def __init__(self, data_dir: str = "../data"):
        """初始化分析器"""
        self.data_dir = Path(data_dir)
        self.survey_data = None
        self.personas_data = None
        
    def load_data(self):
        """加载数据文件"""
        print("正在加载数据...")
        
        # 加载调研数据
        survey_path = self.data_dir / "survey-results.json"
        with open(survey_path, 'r', encoding='utf-8') as f:
            self.survey_data = json.load(f)
        print(f"✓ 已加载调研数据：{self.survey_data['survey_metadata']['total_respondents']} 份问卷")
        
        # 加载用户画像数据
        personas_path = self.data_dir / "user-personas.json"
        with open(personas_path, 'r', encoding='utf-8') as f:
            self.personas_data = json.load(f)
        print(f"✓ 已加载用户画像：{len(self.personas_data['personas'])} 个人物画像")
        
    def analyze_demographics(self) -> Dict:
        """分析人口统计学数据"""
        print("\n=== 人口统计学分析 ===")
        
        demo = self.survey_data['demographics']
        
        # 年龄分布
        print("\n年龄分布：")
        for age_range, pct in demo['age_distribution'].items():
            bar = "█" * int(pct / 2)
            print(f"  {age_range:10s}: {bar} {pct}%")
        
        # 收入分布
        print("\n收入分布：")
        for income_range, pct in demo['income_bracket'].items():
            bar = "█" * int(pct / 2)
            print(f"  {income_range:15s}: {bar} {pct}%")
        
        # 骑行频率
        print("\n骑行频率：")
        for freq, pct in demo['cycling_frequency'].items():
            bar = "█" * int(pct / 2)
            print(f"  {freq:20s}: {bar} {pct}%")
        
        return demo
    
    def analyze_pain_points(self) -> List[Dict]:
        """分析用户痛点"""
        print("\n=== 痛点优先级分析 ===")
        
        pain_points = self.survey_data['pain_points_ranking']
        
        print(f"\n发现 {len(pain_points)} 个主要痛点：\n")
        print(f"{'排名':<6} {'痛点':<30} {'严重程度':<12} {'影响用户':<12}")
        print("-" * 70)
        
        for pp in pain_points:
            severity_bar = "★" * int(pp['severity_score'])
            affected_bar = "●" * int(pp['affected_users_pct'] / 10)
            print(f"{pp['rank']:<6} {pp['pain_point']:<30} {severity_bar:<12} {affected_bar} {pp['affected_users_pct']}%")
        
        # 识别P0级痛点（严重程度≥9.0，影响用户≥80%）
        p0_pain_points = [pp for pp in pain_points 
                          if pp['severity_score'] >= 9.0 and pp['affected_users_pct'] >= 80]
        
        print(f"\n🚨 识别出 {len(p0_pain_points)} 个P0级痛点（必须立即解决）：")
        for pp in p0_pain_points:
            print(f"   • {pp['pain_point']}")
        
        return pain_points
    
    def analyze_feature_importance(self) -> List[Dict]:
        """分析功能重要性"""
        print("\n=== 功能重要性分析 ===")
        
        features = self.survey_data['feature_importance']
        
        # 按重要性排序
        sorted_features = sorted(features, key=lambda x: x['importance_score'], reverse=True)
        
        print(f"\n功能优先级排序：\n")
        print(f"{'功能':<20} {'重要性':<15} {'愿意付费':<15}")
        print("-" * 55)
        
        for feat in sorted_features:
            importance_bar = "█" * int(feat['importance_score'])
            willing_bar = "○" * int(feat['willing_to_pay_extra'] / 10)
            print(f"{feat['feature']:<20} {importance_bar} {feat['importance_score']:.1f}  {willing_bar} {feat['willing_to_pay_extra']}%")
        
        # 识别核心功能（重要性≥8.0，愿意付费≥60%）
        core_features = [f for f in features 
                         if f['importance_score'] >= 8.0 and f['willing_to_pay_extra'] >= 60]
        
        print(f"\n⭐ 识别出 {len(core_features)} 个核心功能（MVP必备）：")
        for feat in core_features:
            print(f"   • {feat['feature']} (重要性: {feat['importance_score']:.1f})")
        
        return features
    
    def analyze_price_sensitivity(self) -> Dict:
        """分析价格敏感度"""
        print("\n=== 价格敏感度分析 ===")
        
        price = self.survey_data['price_sensitivity']
        
        print("\n可接受价格区间分布：\n")
        for range_name, pct in price['acceptable_price_ranges'].items():
            bar = "█" * int(pct / 2)
            print(f"  {range_name:15s}: {bar} {pct}%")
        
        print(f"\n💰 价格甜蜜点：{price['sweet_spot']}")
        print(f"💰 平均可接受价格：₹{price['average_acceptable_price']}")
        
        # 计算累计分布
        cumulative = 0
        print("\n累计市场覆盖：")
        for range_name, pct in price['acceptable_price_ranges'].items():
            cumulative += pct
            print(f"  {range_name:15s}: {cumulative}% 的用户")
        
        return price
    
    def analyze_user_segments(self) -> Dict:
        """分析用户细分"""
        print("\n=== 用户细分分析 ===")
        
        segments = self.survey_data['user_segments']
        
        print("\n用户群体分布：\n")
        total = sum(segments.values())
        for segment, pct in segments.items():
            bar = "█" * int(pct / 2)
            print(f"  {segment:25s}: {bar} {pct}%")
        
        # 从personas获取更详细信息
        print("\n各用户群体特征对比：\n")
        print(f"{'群体':<20} {'市场占比':<12} {'价格区间':<25} {'核心诉求':<30}")
        print("-" * 90)
        
        comparison = self.personas_data['persona_comparison']
        for i, persona in enumerate(self.personas_data['personas']):
            segment_name = persona['archetype']
            segment_size = persona['segment_size']
            price_range = persona['acceptable_price_range']
            key_need = persona['needs'][0] if persona['needs'] else "N/A"
            
            print(f"{segment_name:<20} {segment_size:<12} {price_range:<25} {key_need:<30}")
        
        return segments
    
    def analyze_purchase_barriers(self) -> Dict:
        """分析购买障碍"""
        print("\n=== 购买障碍分析 ===")
        
        barriers = self.survey_data['barriers_to_purchase']
        
        print("\n主要购买障碍：\n")
        # 按百分比排序
        sorted_barriers = sorted(barriers.items(), key=lambda x: x[1], reverse=True)
        
        for barrier, pct in sorted_barriers:
            bar = "█" * int(pct / 2)
            print(f"  {barrier:30s}: {bar} {pct}%")
        
        # 识别关键障碍（>30%）
        critical_barriers = [b for b, p in barriers.items() if p > 30]
        
        print(f"\n🚧 关键购买障碍（需优先解决）：")
        for barrier in critical_barriers:
            print(f"   • {barrier} ({barriers[barrier]}%)")
        
        return barriers
    
    def generate_insights(self) -> List[str]:
        """生成关键洞察"""
        print("\n" + "=" * 70)
        print("=== 关键洞察和建议 ===")
        print("=" * 70)
        
        insights = []
        
        # 洞察1：目标用户
        print("\n1️⃣  目标用户定位")
        print("   • 主要目标：休闲骑行者（占50%市场）")
        print("   • 次要目标：通勤骑行者（占25%市场）")
        print("   • 特征：25-35岁，中等收入，周末骑行，社交分享驱动")
        insights.append("聚焦休闲骑行者（50%市场），这是最大的细分市场")
        
        # 洞察2：核心痛点
        print("\n2️⃣  核心痛点（P0级，必须解决）")
        pain_points = self.survey_data['pain_points_ranking']
        p0_points = [pp for pp in pain_points if pp['severity_score'] >= 9.0]
        for pp in p0_points[:3]:
            print(f"   • {pp['pain_point']} (严重度: {pp['severity_score']:.1f}/10)")
        insights.append("必须同时解决'安全性'和'稳定性'痛点，任何一个不达标都会导致失败")
        
        # 洞察3：价格策略
        print("\n3️⃣  价格策略")
        price_sweet_spot = self.survey_data['price_sensitivity']['sweet_spot']
        print(f"   • 价格甜蜜点：{price_sweet_spot}")
        print("   • 75%的用户可接受₹5,000以下产品")
        print("   • 建议定价：₹3,999-4,999（覆盖主流市场）")
        insights.append(f"定价在{price_sweet_spot}可以覆盖75%的目标市场")
        
        # 洞察4：MVP功能
        print("\n4️⃣  MVP核心功能")
        features = self.survey_data['feature_importance']
        core_features = sorted([f for f in features if f['importance_score'] >= 8.0], 
                              key=lambda x: x['importance_score'], reverse=True)
        for feat in core_features[:5]:
            print(f"   • {feat['feature']} (重要性: {feat['importance_score']:.1f}/10)")
        insights.append("MVP应聚焦：安全固定、稳定防抖、易于安装、手机兼容、画质优化")
        
        # 洞察5：竞争优势
        print("\n5️⃣  差异化竞争优势")
        print("   • 专为印度路况优化的防抖系统")
        print("   • 本地化设计和服务（印地语、泰米尔语等）")
        print("   • 极致性价比（专业设备30%价格，80%效果）")
        print("   • '零手机损坏'承诺（全额赔偿）")
        insights.append("建立'印度设计、印度优化'的本土品牌认知")
        
        # 洞察6：渠道策略
        print("\n6️⃣  营销和渠道策略")
        info_sources = self.survey_data['information_sources']
        top_channels = sorted(info_sources.items(), key=lambda x: x[1], reverse=True)[:3]
        print("   • 主要信息渠道：")
        for channel, pct in top_channels:
            print(f"     - {channel}: {pct}%")
        print("   • 建议：重点投入YouTube评测、Instagram营销、骑行俱乐部合作")
        insights.append("营销聚焦数字渠道（YouTube/Instagram）+ 骑行社群")
        
        # 洞察7：市场进入策略
        print("\n7️⃣  市场进入策略")
        print("   • Phase 1：班加罗尔、浦那试点（骑行文化发达）")
        print("   • Phase 2：德里NCR、孟买、海得拉巴扩展")
        print("   • Phase 3：全国覆盖，Tier 2-3城市")
        print("   • 目标：Year 1 - 15,000台，Year 2 - 80,000台，Year 3 - 200,000台")
        insights.append("采用逐步扩张策略，先在核心城市验证产品-市场匹配度")
        
        return insights
    
    def generate_report(self, output_path: str = "../analysis/data-analysis-report.md"):
        """生成完整分析报告"""
        print("\n正在生成分析报告...")
        
        report = []
        report.append("# 印度骑行拍摄诉求数据分析报告\n")
        report.append(f"**生成时间**：2025年12月18日\n")
        report.append(f"**数据来源**：{self.survey_data['survey_metadata']['total_respondents']} 份用户调研问卷\n")
        report.append("---\n\n")
        
        # 1. 执行摘要
        report.append("## 执行摘要\n\n")
        report.append("本报告基于500份用户调研问卷，深度分析了印度骑行拍摄市场的用户需求和痛点。\n\n")
        
        # 关键发现
        report.append("### 关键发现\n\n")
        report.append("1. **目标市场**：休闲骑行者（50%）和通勤者（25%）是最大的市场机会\n")
        report.append("2. **核心痛点**：安全性（9.5分）、稳定性（9.2分）、价格（9.0分）是三大核心痛点\n")
        report.append("3. **价格甜蜜点**：₹3,000-5,000是最佳定价区间，覆盖75%市场\n")
        report.append("4. **MVP功能**：安全固定、防抖稳定、易于使用是最核心的三大功能\n")
        report.append("5. **市场机会**：当前市场满足度低（仅25% NPS），存在巨大改进空间\n\n")
        
        # 2. 详细分析
        report.append("## 详细数据分析\n\n")
        
        # 人口统计
        report.append("### 用户人口统计\n\n")
        demo = self.survey_data['demographics']
        report.append("**年龄分布**：\n")
        for age, pct in demo['age_distribution'].items():
            report.append(f"- {age}: {pct}%\n")
        report.append("\n")
        
        # 痛点分析
        report.append("### 痛点优先级\n\n")
        report.append("| 排名 | 痛点 | 严重程度 | 影响用户% |\n")
        report.append("|------|------|---------|----------|\n")
        for pp in self.survey_data['pain_points_ranking'][:10]:
            report.append(f"| {pp['rank']} | {pp['pain_point']} | {pp['severity_score']:.1f}/10 | {pp['affected_users_pct']}% |\n")
        report.append("\n")
        
        # 功能重要性
        report.append("### 功能重要性排序\n\n")
        report.append("| 功能 | 重要性评分 | 愿意付费% |\n")
        report.append("|------|-----------|----------|\n")
        features = sorted(self.survey_data['feature_importance'], 
                         key=lambda x: x['importance_score'], reverse=True)
        for feat in features:
            report.append(f"| {feat['feature']} | {feat['importance_score']:.1f}/10 | {feat['willing_to_pay_extra']}% |\n")
        report.append("\n")
        
        # 价格分析
        report.append("### 价格敏感度分析\n\n")
        price = self.survey_data['price_sensitivity']
        report.append(f"**价格甜蜜点**：{price['sweet_spot']}\n\n")
        report.append("**可接受价格分布**：\n")
        for range_name, pct in price['acceptable_price_ranges'].items():
            report.append(f"- {range_name}: {pct}%\n")
        report.append("\n")
        
        # 3. 战略建议
        report.append("## 战略建议\n\n")
        
        report.append("### 产品策略\n\n")
        report.append("1. **MVP定位**：中端性价比产品，定价₹3,999-4,999\n")
        report.append("2. **核心功能**：聚焦安全+稳定+易用三大核心\n")
        report.append("3. **差异化**：专为印度路况和用户习惯优化\n")
        report.append("4. **质量承诺**：'零手机损坏'全额赔偿承诺\n\n")
        
        report.append("### 市场策略\n\n")
        report.append("1. **目标用户**：主攻休闲骑行者（50%市场）\n")
        report.append("2. **试点城市**：班加罗尔、浦那（骑行文化发达）\n")
        report.append("3. **营销渠道**：YouTube评测（65%）+ Instagram（55%）+ 骑行俱乐部（35%）\n")
        report.append("4. **增长策略**：KOL种草 → 口碑传播 → 社群裂变\n\n")
        
        report.append("### 销售目标\n\n")
        report.append("- **Year 1**：15,000台（试点验证）\n")
        report.append("- **Year 2**：80,000台（区域扩展）\n")
        report.append("- **Year 3**：200,000台（全国覆盖）\n\n")
        
        # 写入文件
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(report)
        
        print(f"✓ 报告已生成：{output_path}")
    
    def run_full_analysis(self):
        """运行完整分析"""
        print("=" * 70)
        print("印度骑行拍摄诉求数据分析")
        print("=" * 70)
        
        # 加载数据
        self.load_data()
        
        # 执行各项分析
        self.analyze_demographics()
        self.analyze_pain_points()
        self.analyze_feature_importance()
        self.analyze_price_sensitivity()
        self.analyze_user_segments()
        self.analyze_purchase_barriers()
        
        # 生成洞察
        insights = self.generate_insights()
        
        # 生成报告
        self.generate_report()
        
        print("\n" + "=" * 70)
        print("分析完成！")
        print("=" * 70)


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    # 创建分析器实例
    analyzer = DemandAnalyzer(data_dir=str(data_dir))
    
    # 运行完整分析
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
