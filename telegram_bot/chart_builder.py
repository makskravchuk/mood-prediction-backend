from io import BytesIO

import matplotlib.pyplot as plt

from telegram_bot.schemas import ChartDataCell


class ChartBuilder:

    @classmethod
    def create_pie_chart(cls, data: list[ChartDataCell], title: str) -> BytesIO:
        labels = []
        sizes = []
        colors = []
        for cell in data:
            labels.append(cell.label)
            sizes.append(cell.value)
            colors.append(cell.color)

        plt.rcParams['font.family'] = ['DejaVu Sans', 'Noto Color Emoji']
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', textprops={'fontsize': 12})
        plt.title(title, fontsize=14, fontweight='bold')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return buffer

    @classmethod
    def create_bar_chart(cls, data: list["ChartDataCell"], title: str) -> BytesIO:
        labels = []
        sizes = []
        colors = []

        for cell in data:
            labels.append(cell.label)
            sizes.append(cell.value)
            colors.append(cell.color)

        plt.rcParams['font.family'] = ['DejaVu Sans', 'Noto Color Emoji']
        plt.figure(figsize=(8, 6))
        plt.bar(labels, sizes, color=colors)

        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel("Емоції", fontsize=12)
        plt.ylabel("Кількість", fontsize=12)
        plt.xticks(rotation=30, ha='right', fontsize=12)
        plt.yticks(fontsize=10)

        # Показати значення над стовпчиками
        for i, value in enumerate(sizes):
            value_str = f"{int(value)}%" if value.is_integer() else f"{value:.2f}%"
            plt.text(i, value + 0.02, value_str, ha='center', fontsize=12)

        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return buffer
