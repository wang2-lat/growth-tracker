import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
import uuid

from .models import Experiment
from .storage import Storage
from .analytics import Analytics
from .strategies import show_strategies

app = typer.Typer(help="用户增长实验追踪与渠道分析工具")
console = Console()
storage = Storage()

@app.command()
def add(
    channel: str = typer.Option(..., "--channel", "-c", help="渠道名称"),
    cost: float = typer.Option(..., "--cost", help="投入成本"),
    users: int = typer.Option(..., "--users", "-u", help="获客数"),
    conversions: int = typer.Option(..., "--conversions", "-cv", help="转化数"),
    notes: str = typer.Option(None, "--notes", "-n", help="备注"),
):
    """添加新的增长实验记录"""
    exp = Experiment(
        id=str(uuid.uuid4())[:8],
        channel=channel,
        cost=cost,
        users=users,
        conversions=conversions,
        date=datetime.now().strftime("%Y-%m-%d"),
        notes=notes
    )
    
    storage.add(exp)
    console.print(f"[green]✓[/green] 实验记录已添加 (ID: {exp.id})")
    console.print(f"  CAC: ¥{exp.cac:.2f} | 转化率: {exp.conversion_rate:.1f}% | ROI: {exp.roi:.1f}%")

@app.command()
def list():
    """列出所有实验记录"""
    experiments = storage.load()
    
    if not experiments:
        console.print("[yellow]暂无实验记录[/yellow]")
        return
    
    table = Table(title="增长实验记录")
    table.add_column("ID", style="cyan")
    table.add_column("渠道", style="magenta")
    table.add_column("日期")
    table.add_column("投入", justify="right")
    table.add_column("获客", justify="right")
    table.add_column("转化", justify="right")
    table.add_column("CAC", justify="right")
    table.add_column("转化率", justify="right")
    table.add_column("ROI", justify="right")
    
    for exp in sorted(experiments, key=lambda x: x.date, reverse=True):
        table.add_row(
            exp.id,
            exp.channel,
            exp.date,
            f"¥{exp.cost:.2f}",
            str(exp.users),
            str(exp.conversions),
            f"¥{exp.cac:.2f}",
            f"{exp.conversion_rate:.1f}%",
            f"{exp.roi:.1f}%"
        )
    
    console.print(table)

@app.command()
def delete(exp_id: str = typer.Argument(..., help="实验 ID")):
    """删除实验记录"""
    if storage.delete(exp_id):
        console.print(f"[green]✓[/green] 实验记录已删除 (ID: {exp_id})")
    else:
        console.print(f"[red]✗[/red] 未找到 ID 为 {exp_id} 的实验记录")

@app.command()
def report(
    format: str = typer.Option("markdown", "--format", "-f", help="报告格式: markdown 或 csv"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """生成渠道效果对比报告"""
    experiments = storage.load()
    
    if not experiments:
        console.print("[yellow]暂无实验数据，无法生成报告[/yellow]")
        return
    
    if format == "markdown":
        content = Analytics.generate_markdown_report(experiments)
        default_file = f"growth_report_{datetime.now().strftime('%Y%m%d')}.md"
    elif format == "csv":
        content = Analytics.generate_csv_report(experiments)
        default_file = f"growth_report_{datetime.now().strftime('%Y%m%d')}.csv"
    else:
        console.print("[red]不支持的格式，请使用 markdown 或 csv[/red]")
        return
    
    output_file = output or default_file
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    console.print(f"[green]✓[/green] 报告已生成: {output_file}")

@app.command()
def strategies():
    """查看低成本获客策略清单"""
    console.print(show_strategies())

@app.command()
def summary():
    """显示总体数据摘要"""
    experiments = storage.load()
    
    if not experiments:
        console.print("[yellow]暂无实验数据[/yellow]")
        return
    
    total_cost = sum(exp.cost for exp in experiments)
    total_users = sum(exp.users for exp in experiments)
    total_conversions = sum(exp.conversions for exp in experiments)
    avg_cac = total_cost / total_users if total_users > 0 else 0
    avg_conversion = total_conversions / total_users * 100 if total_users > 0 else 0
    
    console.print("\n[bold]📊 增长数据总览[/bold]\n")
    console.print(f"总实验数: [cyan]{len(experiments)}[/cyan]")
    console.print(f"总投入: [yellow]¥{total_cost:.2f}[/yellow]")
    console.print(f"总获客: [green]{total_users}[/green] 人")
    console.print(f"总转化: [green]{total_conversions}[/green] 人")
    console.print(f"平均 CAC: [yellow]¥{avg_cac:.2f}[/yellow]")
    console.print(f"平均转化率: [cyan]{avg_conversion:.1f}%[/cyan]\n")

if __name__ == "__main__":
    app()