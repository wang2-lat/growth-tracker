from typing import List
from collections import defaultdict
from .models import Experiment

class Analytics:
    """数据分析与报告生成"""
    
    @staticmethod
    def generate_markdown_report(experiments: List[Experiment]) -> str:
        """生成 Markdown 格式报告"""
        if not experiments:
            return "# 增长实验报告\n\n暂无数据"
        
        # 按渠道汇总
        channel_stats = defaultdict(lambda: {"cost": 0, "users": 0, "conversions": 0, "count": 0})
        
        for exp in experiments:
            stats = channel_stats[exp.channel]
            stats["cost"] += exp.cost
            stats["users"] += exp.users
            stats["conversions"] += exp.conversions
            stats["count"] += 1
        
        # 生成报告
        report = ["# 增长实验报告\n"]
        report.append(f"**总实验数**: {len(experiments)}\n")
        report.append(f"**总投入**: ¥{sum(exp.cost for exp in experiments):.2f}\n")
        report.append(f"**总获客**: {sum(exp.users for exp in experiments)} 人\n")
        report.append(f"**总转化**: {sum(exp.conversions for exp in experiments)} 人\n\n")
        
        report.append("## 渠道效果对比\n")
        report.append("| 渠道 | 实验次数 | 总投入 | 获客数 | 转化数 | 平均CAC | 转化率 | ROI |\n")
        report.append("|------|---------|--------|--------|--------|---------|--------|-----|\n")
        
        for channel, stats in sorted(channel_stats.items(), key=lambda x: x[1]["users"], reverse=True):
            cac = stats["cost"] / stats["users"] if stats["users"] > 0 else 0
            conv_rate = stats["conversions"] / stats["users"] * 100 if stats["users"] > 0 else 0
            revenue = stats["conversions"] * 100
            roi = (revenue - stats["cost"]) / stats["cost"] * 100 if stats["cost"] > 0 else 0
            
            report.append(f"| {channel} | {stats['count']} | ¥{stats['cost']:.2f} | {stats['users']} | {stats['conversions']} | ¥{cac:.2f} | {conv_rate:.1f}% | {roi:.1f}% |\n")
        
        report.append("\n## 详细实验记录\n")
        for exp in sorted(experiments, key=lambda x: x.date, reverse=True):
            report.append(f"\n### {exp.channel} - {exp.date}\n")
            report.append(f"- **投入**: ¥{exp.cost:.2f}\n")
            report.append(f"- **获客**: {exp.users} 人\n")
            report.append(f"- **转化**: {exp.conversions} 人\n")
            report.append(f"- **CAC**: ¥{exp.cac:.2f}\n")
            report.append(f"- **转化率**: {exp.conversion_rate:.1f}%\n")
            report.append(f"- **ROI**: {exp.roi:.1f}%\n")
            if exp.notes:
                report.append(f"- **备注**: {exp.notes}\n")
        
        return "".join(report)
    
    @staticmethod
    def generate_csv_report(experiments: List[Experiment]) -> str:
        """生成 CSV 格式报告"""
        lines = ["渠道,日期,投入成本,获客数,转化数,CAC,转化率(%),ROI(%),备注"]
        
        for exp in experiments:
            lines.append(
                f"{exp.channel},{exp.date},{exp.cost:.2f},{exp.users},{exp.conversions},"
                f"{exp.cac:.2f},{exp.conversion_rate:.2f},{exp.roi:.2f},{exp.notes or ''}"
            )
        
        return "\n".join(lines)