#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
印度骑行拍摄诉求数据可视化脚本

功能：
1. 生成各类数据可视化图表
2. 导出为PNG/SVG格式
3. 创建交互式HTML报告

依赖：matplotlib, seaborn（需安装）
安装：pip install matplotlib seaborn

作者：印度骑行拍摄诉求分析项目组
日期：2025-12-18
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# 检查依赖
try:
    import matplotlib
    matplotlib.use('Agg')  # 无GUI后端
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
except ImportError:
    print("警告：matplotlib未安装，将跳过图表生成")
    print("安装命令：pip install matplotlib")
    HAS_MATPLOTLIB = False
else:
    HAS_MATPLOTLIB = True


class DataVisualizer:
    """数据可视化器"""
    
    def __init__(self, data_dir: str = "../data", output_dir: str = "../analysis/charts"):
        """初始化可视化器"""
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.survey_data = None
        self.personas_data = None
        
    def load_data(self):
        """加载数据"""
        print("正在加载数据...")
        
        survey_path = self.data_dir / "survey-results.json"
        with open(survey_path, 'r', encoding='utf-8') as f:
            self.survey_data = json.load(f)
        
        personas_path = self.data_dir / "user-personas.json"
        with open(personas_path, 'r', encoding='utf-8') as f:
            self.personas_data = json.load(f)
        
        print("✓ 数据加载完成")
    
    def plot_pain_points(self):
        """绘制痛点分析图"""
        if not HAS_MATPLOTLIB:
            return
        
        print("正在生成痛点分析图...")
        
        pain_points = self.survey_data['pain_points_ranking'][:10]
        
        # 提取数据
        labels = [pp['pain_point'] for pp in pain_points]
        severity = [pp['severity_score'] for pp in pain_points]
        affected = [pp['affected_users_pct'] for pp in pain_points]
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 严重程度
        colors1 = ['#d32f2f' if s >= 9.0 else '#f57c00' if s >= 8.0 else '#fbc02d' 
                   for s in severity]
        ax1.barh(labels, severity, color=colors1, alpha=0.8)
        ax1.set_xlabel('Severity Score', fontsize=12)
        ax1.set_title('Pain Points by Severity', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 10)
        ax1.grid(axis='x', alpha=0.3)
        
        # 影响用户百分比
        colors2 = ['#d32f2f' if a >= 80 else '#f57c00' if a >= 60 else '#fbc02d' 
                   for a in affected]
        ax2.barh(labels, affected, color=colors2, alpha=0.8)
        ax2.set_xlabel('Affected Users (%)', fontsize=12)
        ax2.set_title('Pain Points by User Impact', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 100)
        ax2.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        # 保存
        output_path = self.output_dir / "pain_points_analysis.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 痛点分析图已保存：{output_path}")
    
    def plot_feature_importance(self):
        """绘制功能重要性图"""
        if not HAS_MATPLOTLIB:
            return
        
        print("正在生成功能重要性图...")
        
        features = sorted(self.survey_data['feature_importance'], 
                         key=lambda x: x['importance_score'], reverse=True)
        
        # 提取数据
        labels = [f['feature'] for f in features]
        importance = [f['importance_score'] for f in features]
        willing_pay = [f['willing_to_pay_extra'] for f in features]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x = range(len(labels))
        width = 0.35
        
        bars1 = ax.barh([i - width/2 for i in x], importance, width, 
                        label='Importance Score', color='#1976d2', alpha=0.8)
        bars2 = ax.barh([i + width/2 for i in x], [w/10 for w in willing_pay], width,
                        label='Willing to Pay (normalized)', color='#388e3c', alpha=0.8)
        
        ax.set_yticks(x)
        ax.set_yticklabels(labels)
        ax.set_xlabel('Score', fontsize=12)
        ax.set_title('Feature Importance & Willingness to Pay', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        # 保存
        output_path = self.output_dir / "feature_importance.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 功能重要性图已保存：{output_path}")
    
    def plot_price_sensitivity(self):
        """绘制价格敏感度图"""
        if not HAS_MATPLOTLIB:
            return
        
        print("正在生成价格敏感度图...")
        
        price = self.survey_data['price_sensitivity']
        ranges = price['acceptable_price_ranges']
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # 饼图
        labels = list(ranges.keys())
        sizes = list(ranges.values())
        colors = ['#2196f3', '#4caf50', '#ffc107', '#ff9800', '#f44336']
        
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Acceptable Price Distribution', fontsize=14, fontweight='bold')
        
        # 累计分布图
        cumulative = []
        cum_sum = 0
        for size in sizes:
            cum_sum += size
            cumulative.append(cum_sum)
        
        ax2.plot(labels, cumulative, marker='o', linewidth=2, markersize=8, color='#1976d2')
        ax2.fill_between(range(len(labels)), cumulative, alpha=0.3, color='#1976d2')
        ax2.set_ylabel('Cumulative Coverage (%)', fontsize=12)
        ax2.set_title('Cumulative Market Coverage by Price', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 105)
        
        # 添加甜蜜点标注
        ax2.axhline(y=75, color='red', linestyle='--', alpha=0.5, label='Target: 75%')
        ax2.legend()
        
        plt.tight_layout()
        
        # 保存
        output_path = self.output_dir / "price_sensitivity.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 价格敏感度图已保存：{output_path}")
    
    def plot_user_segments(self):
        """绘制用户细分图"""
        if not HAS_MATPLOTLIB:
            return
        
        print("正在生成用户细分图...")
        
        segments = self.survey_data['user_segments']
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))
        
        labels = list(segments.keys())
        sizes = list(segments.values())
        colors = ['#e91e63', '#9c27b0', '#3f51b5', '#009688']
        explode = (0.1, 0, 0, 0)  # 突出显示最大的部分
        
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, 
                                           autopct='%1.1f%%', colors=colors, 
                                           startangle=90, textprops={'fontsize': 11})
        
        # 美化标签
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('User Segment Distribution', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # 保存
        output_path = self.output_dir / "user_segments.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 用户细分图已保存：{output_path}")
    
    def plot_demographics(self):
        """绘制人口统计图"""
        if not HAS_MATPLOTLIB:
            return
        
        print("正在生成人口统计图...")
        
        demo = self.survey_data['demographics']
        
        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 年龄分布
        age_dist = demo['age_distribution']
        ax1.bar(age_dist.keys(), age_dist.values(), color='#3f51b5', alpha=0.8)
        ax1.set_ylabel('Percentage (%)')
        ax1.set_title('Age Distribution', fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. 收入分布
        income_dist = demo['income_bracket']
        ax2.barh(list(income_dist.keys()), list(income_dist.values()), color='#4caf50', alpha=0.8)
        ax2.set_xlabel('Percentage (%)')
        ax2.set_title('Income Distribution', fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        # 3. 骑行频率
        freq_dist = demo['cycling_frequency']
        colors = ['#f44336', '#ff9800', '#ffc107', '#8bc34a', '#4caf50']
        ax3.pie(freq_dist.values(), labels=freq_dist.keys(), autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax3.set_title('Cycling Frequency', fontweight='bold')
        
        # 4. 性别分布
        gender_dist = demo['gender']
        ax4.bar(gender_dist.keys(), gender_dist.values(), color=['#2196f3', '#e91e63', '#9e9e9e'], 
               alpha=0.8)
        ax4.set_ylabel('Percentage (%)')
        ax4.set_title('Gender Distribution', fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # 保存
        output_path = self.output_dir / "demographics.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 人口统计图已保存：{output_path}")
    
    def plot_purchase_barriers(self):
        """绘制购买障碍图"""
        if not HAS_MATPLOTLIB:
            return
        
        print("正在生成购买障碍图...")
        
        barriers = self.survey_data['barriers_to_purchase']
        sorted_barriers = sorted(barriers.items(), key=lambda x: x[1], reverse=True)
        
        labels = [b[0] for b in sorted_barriers]
        values = [b[1] for b in sorted_barriers]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        
        colors = ['#d32f2f' if v >= 40 else '#f57c00' if v >= 25 else '#fbc02d' 
                 for v in values]
        
        bars = ax.barh(labels, values, color=colors, alpha=0.8)
        ax.set_xlabel('Percentage of Users (%)', fontsize=12)
        ax.set_title('Purchase Barriers', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{width:.0f}%', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        
        # 保存
        output_path = self.output_dir / "purchase_barriers.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ 购买障碍图已保存：{output_path}")
    
    def generate_html_report(self):
        """生成HTML可视化报告"""
        print("正在生成HTML报告...")
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>印度骑行拍摄诉求分析 - 可视化报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { font-size: 1.2em; opacity: 0.9; }
        .section {
            background: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .insight-box {
            background: #e8eaf6;
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 4px;
        }
        .insight-box h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        .stat-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚴 印度骑行拍摄诉求分析</h1>
            <p class="subtitle">数据可视化报告 | 2025年12月18日</p>
        </header>
        
        <div class="section">
            <h2>📊 核心数据概览</h2>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-label">调研样本</div>
                    <div class="stat-value">500</div>
                    <div class="stat-label">份问卷</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">目标市场</div>
                    <div class="stat-value">1500万</div>
                    <div class="stat-label">潜在用户</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">价格甜蜜点</div>
                    <div class="stat-value">₹3-5K</div>
                    <div class="stat-label">覆盖75%市场</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">NPS得分</div>
                    <div class="stat-value">25</div>
                    <div class="stat-label">改进空间巨大</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>👥 用户细分</h2>
            <div class="chart-container">
                <img src="charts/user_segments.png" alt="用户细分">
            </div>
            <div class="insight-box">
                <h3>💡 关键洞察</h3>
                <p><strong>休闲骑行者（50%）</strong>是最大的细分市场，应作为主要目标用户。
                这个群体注重<strong>性价比、易用性和社交分享</strong>，对价格敏感，
                理想价格区间为₹2,000-8,000。</p>
            </div>
        </div>
        
        <div class="section">
            <h2>⚠️ 核心痛点分析</h2>
            <div class="chart-container">
                <img src="charts/pain_points_analysis.png" alt="痛点分析">
            </div>
            <div class="insight-box">
                <h3>💡 P0级痛点（必须解决）</h3>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><strong>安全性问题</strong> (9.5/10) - 85%用户担心手机脱落损坏</li>
                    <li><strong>画面抖动</strong> (9.2/10) - 90%用户反馈视频抖动严重</li>
                    <li><strong>价格昂贵</strong> (9.0/10) - 80%用户认为现有产品太贵</li>
                </ul>
                <p style="margin-top: 10px;">这三个痛点必须同时解决，任何一个不达标都会导致产品失败。</p>
            </div>
        </div>
        
        <div class="section">
            <h2>⭐ 功能重要性</h2>
            <div class="chart-container">
                <img src="charts/feature_importance.png" alt="功能重要性">
            </div>
            <div class="insight-box">
                <h3>💡 MVP核心功能</h3>
                <p>MVP产品应聚焦以下<strong>高重要性+高付费意愿</strong>的功能：</p>
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>安全固定系统 (9.5分, 85%愿意付费)</li>
                    <li>防抖稳定功能 (9.2分, 78%愿意付费)</li>
                    <li>易于安装使用 (8.8分, 65%愿意付费)</li>
                    <li>画质优化 (8.2分, 52%愿意付费)</li>
                </ol>
            </div>
        </div>
        
        <div class="section">
            <h2>💰 价格敏感度</h2>
            <div class="chart-container">
                <img src="charts/price_sensitivity.png" alt="价格敏感度">
            </div>
            <div class="insight-box">
                <h3>💡 定价策略</h3>
                <p><strong>建议定价：₹3,999 - ₹4,999</strong></p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>覆盖75%的目标市场（₹5,000以下）</li>
                    <li>避开低端市场的质量顾虑</li>
                    <li>保持足够的利润空间（55%毛利率）</li>
                    <li>与高端品牌形成差异化（仅为GoPro的1/7价格）</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>🚧 购买障碍</h2>
            <div class="chart-container">
                <img src="charts/purchase_barriers.png" alt="购买障碍">
            </div>
            <div class="insight-box">
                <h3>💡 破除障碍策略</h3>
                <ul style="margin-left: 20px;">
                    <li><strong>价格太贵 (52%)</strong> → 定价₹3,999，提供极致性价比</li>
                    <li><strong>质量不确定 (35%)</strong> → 提供试用、"零手机损坏"承诺、2年保修</li>
                    <li><strong>不知道买什么 (30%)</strong> → 简化产品线，提供选购指南和对比工具</li>
                    <li><strong>担心手机损坏 (28%)</strong> → 全额赔偿承诺+保险合作</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 人口统计分析</h2>
            <div class="chart-container">
                <img src="charts/demographics.png" alt="人口统计">
            </div>
            <div class="insight-box">
                <h3>💡 目标用户画像</h3>
                <p><strong>核心用户特征</strong>：</p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>年龄：25-35岁（63%）</li>
                    <li>收入：₹350K-750K（50%）</li>
                    <li>骑行频率：每周1-5次（65%）</li>
                    <li>性别：男性为主（72%），女性市场有增长潜力</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 战略建议总结</h2>
            <div class="insight-box">
                <h3>1. 产品策略</h3>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>MVP定位：中端性价比产品，定价₹3,999</li>
                    <li>核心功能：安全+稳定+易用三大核心</li>
                    <li>差异化：专为印度路况和用户习惯优化</li>
                    <li>质量承诺："零手机损坏"全额赔偿</li>
                </ul>
            </div>
            
            <div class="insight-box">
                <h3>2. 市场策略</h3>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>目标用户：主攻休闲骑行者（50%市场）</li>
                    <li>试点城市：班加罗尔、浦那</li>
                    <li>营销渠道：YouTube评测 + Instagram + 骑行俱乐部</li>
                    <li>增长策略：KOL种草 → 口碑传播 → 社群裂变</li>
                </ul>
            </div>
            
            <div class="insight-box">
                <h3>3. 销售目标</h3>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li><strong>Year 1</strong>：15,000台（试点验证）</li>
                    <li><strong>Year 2</strong>：80,000台（区域扩展）</li>
                    <li><strong>Year 3</strong>：200,000台（全国覆盖）</li>
                </ul>
            </div>
        </div>
        
        <footer>
            <p>© 2025 印度骑行拍摄诉求分析项目组 | 数据来源：500份用户调研问卷</p>
        </footer>
    </div>
</body>
</html>"""
        
        # 保存HTML
        output_path = self.output_dir.parent / "visualization-report.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ HTML报告已生成：{output_path}")
    
    def run_all_visualizations(self):
        """运行所有可视化"""
        print("=" * 70)
        print("印度骑行拍摄诉求数据可视化")
        print("=" * 70)
        
        self.load_data()
        
        if HAS_MATPLOTLIB:
            print("\n正在生成图表...")
            self.plot_user_segments()
            self.plot_pain_points()
            self.plot_feature_importance()
            self.plot_price_sensitivity()
            self.plot_demographics()
            self.plot_purchase_barriers()
            print("\n✓ 所有图表生成完成！")
        else:
            print("\n⚠️  matplotlib未安装，跳过图表生成")
        
        self.generate_html_report()
        
        print("\n" + "=" * 70)
        print("可视化完成！")
        print("=" * 70)
        print(f"\n查看结果：")
        print(f"  • 图表目录：{self.output_dir}")
        print(f"  • HTML报告：{self.output_dir.parent / 'visualization-report.html'}")


def main():
    """主函数"""
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    output_dir = script_dir.parent / "analysis" / "charts"
    
    visualizer = DataVisualizer(data_dir=str(data_dir), output_dir=str(output_dir))
    visualizer.run_all_visualizations()


if __name__ == "__main__":
    main()
