import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# =============================
# CẤU HÌNH TRANG
# =============================
st.set_page_config(
    page_title="Phân bổ & tăng trưởng doanh thu",
    layout="wide"
)

st.title("📊 PHÂN BỔ DOANH THU & TĂNG TRƯỞNG 2025–2026")
st.caption("Doanh thu 2025 tùy chỉnh – tổng năm luôn cố định | 2026 tính theo % tăng trưởng")

# =============================
# THÔNG TIN DOANH NGHIỆP
# =============================
with st.sidebar:
    st.header("🏢 Thông tin doanh nghiệp")
    ten_dn = st.text_input("Tên doanh nghiệp")
    mst = st.text_input("Mã số thuế")

# =============================
# TỔNG DOANH THU 2025
# =============================
tong_2025 = st.number_input(
    "Tổng doanh thu năm 2025 (VNĐ)",
    min_value=0,
    value=12_000_000_000,
    step=100_000_000
)

months = [f"Tháng {i}" for i in range(1, 13)]

# =============================
# KHỞI TẠO SESSION STATE
# =============================
if "dt_2025" not in st.session_state:
    w = np.random.uniform(0.7, 1.3, 12)
    w = w / w.sum()
    dt = np.round(w * tong_2025, 0)
    dt[-1] += tong_2025 - dt.sum()
    st.session_state.dt_2025 = dt.astype(int)

if "growth" not in st.session_state:
    st.session_state.growth = np.array([5.0] * 12)

# =============================
# HÀM CÂN BẰNG LẠI DOANH THU 2025
# =============================
def rebalance_2025(df_edit, total):
    values = df_edit["DT 2025"].values.astype(float)
    fixed_mask = df_edit["Khóa"].values

    fixed_sum = values[fixed_mask].sum()
    remain = total - fixed_sum

    if remain < 0:
        st.error("❌ Tổng các tháng khóa vượt tổng năm 2025")
        return values.astype(int)

    free_idx = np.where(~fixed_mask)[0]
    if len(free_idx) == 0:
        return values.astype(int)

    weights = values[free_idx]
    weights = weights / weights.sum() if weights.sum() > 0 else np.ones(len(free_idx)) / len(free_idx)

    values[free_idx] = np.round(weights * remain, 0)
    values[-1] += total - values.sum()

    return values.astype(int)

# =============================
# BẢNG NHẬP DOANH THU 2025
# =============================
st.subheader("📅 Doanh thu năm 2025 theo tháng")

df_2025 = pd.DataFrame({
    "Tháng": months,
    "DT 2025": st.session_state.dt_2025,
    "Khóa": [False] * 12
})

edited_2025 = st.data_editor(
    df_2025,
    hide_index=True,
    use_container_width=True,
    column_config={
        "DT 2025": st.column_config.NumberColumn(step=10_000_000),
        "Khóa": st.column_config.CheckboxColumn("Giữ cố định tháng")
    },
    key="editor_2025"
)

if st.button("🔁 Cân đối lại doanh thu 2025"):
    st.session_state.dt_2025 = rebalance_2025(edited_2025, tong_2025)
    st.success("Đã tự động cân đối – tổng năm 2025 luôn chính xác")

# =============================
# NHẬP TĂNG TRƯỞNG %
# =============================
st.subheader("📈 Tăng trưởng % năm 2026 so với 2025")

df_growth = pd.DataFrame({
    "Tháng": months,
    "Tăng trưởng (%)": st.session_state.growth
})

edited_growth = st.data_editor(
    df_growth,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Tăng trưởng (%)": st.column_config.NumberColumn(
            min_value=-50.0,
            max_value=200.0,
            step=0.1
        )
    },
    key="growth_editor"
)

if st.button("📌 Áp dụng tăng trưởng"):
    st.session_state.growth = edited_growth["Tăng trưởng (%)"].values
    st.success("Đã cập nhật tăng trưởng 2026")

# =============================
# TÍNH DOANH THU 2026
# =============================
dt_2025 = st.session_state.dt_2025
growth = st.session_state.growth

dt_2026 = np.round(dt_2025 * (1 + growth / 100), 0).astype(int)

df_month = pd.DataFrame({
    "Tháng": months,
    "DT 2025": dt_2025,
    "Tăng trưởng (%)": growth,
    "DT 2026": dt_2026
})

st.subheader("📊 Kết quả theo tháng")

st.dataframe(df_month, use_container_width=True)

# =============================
# TỔNG HỢP
# =============================
def tong_hop(df, label, start, end):
    v25 = df.iloc[start:end]["DT 2025"].sum()
    v26 = df.iloc[start:end]["DT 2026"].sum()
    rate = (v26 / v25 - 1) * 100 if v25 > 0 else 0
    return [label, v25, v26, rate]

summary = [
    tong_hop(df_month, "Quý I", 0, 3),
    tong_hop(df_month, "Quý II", 3, 6),
    tong_hop(df_month, "Quý III", 6, 9),
    tong_hop(df_month, "Quý IV", 9, 12),
    tong_hop(df_month, "6 tháng", 0, 6),
    tong_hop(df_month, "9 tháng", 0, 9),
    tong_hop(df_month, "Cả năm", 0, 12),
]

df_summary = pd.DataFrame(
    summary,
    columns=["Kỳ", "DT 2025", "DT 2026", "Tăng trưởng (%)"]
)

st.subheader("📌 Tổng hợp theo kỳ")
st.dataframe(df_summary, use_container_width=True)

# =============================
# XUẤT EXCEL
# =============================
def export_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_month.to_excel(writer, index=False, sheet_name="Theo tháng")
        df_summary.to_excel(writer, index=False, sheet_name="Tổng hợp")
        pd.DataFrame({
            "Thông tin": ["Tên DN", "MST", "Tổng DT 2025", "Tổng DT 2026"],
            "Giá trị": [
                ten_dn,
                mst,
                df_month["DT 2025"].sum(),
                df_month["DT 2026"].sum()
            ]
        }).to_excel(writer, index=False, sheet_name="Doanh nghiệp")
    output.seek(0)
    return output

st.download_button(
    "⬇️ Xuất Excel",
    data=export_excel(),
    file_name="Doanh_thu_2025_2026.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
