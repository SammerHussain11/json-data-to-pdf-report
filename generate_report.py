import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

def create_bar_chart(data):
    df = pd.DataFrame(data).T
    individuals = [key for key in df.columns if key != "average_score"]
    num_people = len(individuals)
    num_attributes = len(df)

    # Increase figure height based on number of people (bigger than before)
    fig_height = 2 + 0.6 * num_attributes  # makes graph taller for more rows
    fig, ax = plt.subplots(figsize=(12, fig_height))  # wider and taller graph

    # Bar width and horizontal positioning
    bar_width = 0.8 / num_people
    y_positions = list(range(num_attributes))

    # Plot each individual's bar
    for i, person in enumerate(individuals):
        offset_y = [y + i * bar_width for y in y_positions]
        ax.barh(offset_y, df[person], height=bar_width, label=person, alpha=0.8)

    # ✅ Plot average line correctly aligned with center of bars
    avg_line_y = [y + (bar_width * num_people) / 2 for y in y_positions]
    ax.plot(df['average_score'], avg_line_y, 'r-', label="Average", linewidth=2)

    # Configure axis
    ax.set_yticks(avg_line_y)
    ax.set_yticklabels(df.index)
    ax.set_xlabel('Scores')
    ax.set_xlim(0, 10)
    ax.legend(loc='upper right', fontsize='small')
    ax.set_title("Performance Comparison")

    plt.tight_layout()
    chart_path = "chart.png"
    plt.savefig(chart_path, bbox_inches="tight", dpi=300)  # high quality
    plt.close()
    return chart_path

def create_pdf_report(data):
    chart_path = create_bar_chart(data)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Performance Report", ln=True, align="C")
    pdf.image(chart_path, x=10, y=30, w=190)  # fit to page width

    pdf.output("report.pdf")
