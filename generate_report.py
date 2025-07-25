import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from fpdf import FPDF
from matplotlib import cm
import math

# ---- Create Bar Chart (Fixed Look) ----
def create_bar_chart(data, page_num=1, attr_page_size=12, people_page_size=3):
    df = pd.DataFrame(data).T
    individuals = [col for col in df.columns if col != "average_score"]
    num_people = len(individuals)
    attributes = df.index.tolist()

    # --- Pagination for attributes (rows) ---
    attr_start = (page_num - 1) * attr_page_size
    attr_end = attr_start + attr_page_size
    page_attributes = attributes[attr_start:attr_end]

    # --- Split people into groups (fixed width for 3 people) ---
    num_people_groups = math.ceil(num_people / people_page_size)
    charts = []

    for group in range(num_people_groups):
        start_idx = group * people_page_size
        end_idx = start_idx + people_page_size
        group_people = individuals[start_idx:end_idx]

        # Create sub-DataFrame with fixed group of people
        df_page = df.loc[page_attributes, group_people + ['average_score']]

        # Fixed height regardless of people count
        fig_height = 0.55 * len(df_page) + 2
        fig, ax = plt.subplots(figsize=(8.27, fig_height))  # A4 width ~8.27in

        # Background color
        ax.set_facecolor("#e6fff7")
        fig.patch.set_facecolor("white")

        # Bar width
        bar_width = 0.8 / len(group_people)
        y_positions = np.arange(len(df_page))
        avg_line_y = y_positions + (bar_width * len(group_people)) / 2

        # Purple bars
        purple_colors = cm.plasma(np.linspace(0.4, 0.8, len(group_people)))
        for i, person in enumerate(group_people):
            ax.barh(
                y_positions + i * bar_width,
                df_page[person],
                height=bar_width,
                color=purple_colors[i],
                alpha=0.9
            )

        # Red average line
        ax.plot(df_page['average_score'], avg_line_y, color='red', linewidth=2)

        # Right-side names + average
        for i, (attr, row) in enumerate(df_page.iterrows()):
            avg_score = row['average_score']
            names_text = "\n".join(group_people)
            text = f"{names_text}   average_scores: {avg_score:.1f}"
            ax.text(10.2, avg_line_y[i], text,
                    va='center', ha='left', fontsize=8)

        # Y-axis labels (attributes)
        ax.set_yticks(avg_line_y)
        ax.set_yticklabels(page_attributes, fontsize=9)
        ax.invert_yaxis()

        # Clean axis
        ax.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        ax.set_xlim(0, 11)
        ax.set_xticks([])

        plt.tight_layout()

        chart_path = f"chart_page_{page_num}_group_{group + 1}.png"
        plt.savefig(chart_path, bbox_inches="tight", dpi=300)
        plt.close()

        charts.append(chart_path)

    # Determine if more attribute pages exist
    more_pages = len(attributes) > attr_end
    return charts, more_pages


# ---- Generate PDF with multiple pages ----
def create_pdf_report(data):
    pdf = FPDF(orientation='P', unit='mm', format='A4')  # A4 for mobile compatibility
    page_num = 1
    more_pages = True

    while more_pages:
        chart_paths, more_pages = create_bar_chart(data, page_num=page_num)

        for chart_path in chart_paths:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Performance Report", ln=True, align="C")

            # Fit image to full page width (keeping same look on mobile/laptop)
            pdf.image(chart_path, x=10, y=30, w=190)

        page_num += 1

    pdf.output("report.pdf")
