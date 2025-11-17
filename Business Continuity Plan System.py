import streamlit as st
import json
import os

# -------------------------------
# تحميل البيانات من ملف JSON
# -------------------------------
def load_data():
    if os.path.exists("bcp_data.json"):
        try:
            with open("bcp_data.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return {"risks": [], "plans": []}
    else:
        return {"risks": [], "plans": []}

# -------------------------------
# حفظ البيانات
# -------------------------------
def save_data(data):
    with open("bcp_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# -------------------------------
# إضافة خطر جديد
# -------------------------------
def add_risk(data, name, impact, probability):
    new_risk = {
        "name": name,
        "impact": impact,
        "probability": probability
    }
    data["risks"].append(new_risk)
    save_data(data)

# -------------------------------
# إضافة خطة طوارئ
# -------------------------------
def add_plan(data, risk_name, steps, responsible):
    new_plan = {
        "risk": risk_name,
        "steps": steps,
        "responsible": responsible
    }
    data["plans"].append(new_plan)
    save_data(data)

# -------------------------------
# الصفحة الرئيسية
# -------------------------------
st.set_page_config(page_title="Business Continuity System", layout="wide")

st.title("🛡 نظام إدارة استمرارية العمل - Business Continuity Plan System")
st.write("إدارة مخاطر الشركة وتجهيز خطط الطوارئ والحفاظ على استمرارية العمل.")

data = load_data()

tabs = st.tabs([
    "📌 إضافة خطر",
    "⚠ عرض كل المخاطر",
    "🧩 إضافة خطة طوارئ",
    "📘 عرض كل الخطط",
    "🔍 البحث",
    "✔ مراجعة النظام"
])

# ----------------------------------------
# TAB 1 : Add Risk
# ----------------------------------------
with tabs[0]:
    st.subheader("📌 إضافة خطر جديد")

    risk_name = st.text_input("اسم الخطر:")
    impact = st.selectbox("درجة التأثير:", ["منخفض", "متوسط", "عالي"])
    probability = st.selectbox("احتمالية الحدوث:", ["ضعيف", "متوسط", "عالي"])

    if st.button("إضافة الخطر"):
        if risk_name.strip() == "":
            st.error("من فضلك أدخل اسم الخطر.")
        else:
            add_risk(data, risk_name, impact, probability)
            st.success("تم إضافة الخطر بنجاح ✔")

# ----------------------------------------
# TAB 2 : Show Risks
# ----------------------------------------
with tabs[1]:
    st.subheader("⚠ قائمة المخاطر المسجلة")
    if len(data["risks"]) == 0:
        st.info("لا يوجد مخاطر مسجلة بعد.")
    else:
        for r in data["risks"]:
            st.write(f"### 🔸 {r['name']}")
            st.write(f"- التأثير: {r['impact']}")
            st.write(f"- الاحتمالية: {r['probability']}")
            st.markdown("---")

# ----------------------------------------
# TAB 3 : Add Plan
# ----------------------------------------
with tabs[2]:
    st.subheader("🧩 إضافة خطة طوارئ")

    if len(data["risks"]) == 0:
        st.warning("لا يمكن إضافة خطة لأنه لا توجد مخاطر مسجلة.")
    else:
        risk_list = [r["name"] for r in data["risks"]]
        selected_risk = st.selectbox("اختر الخطر:", risk_list)

        steps = st.text_area("خطوات الخطة:")
        responsible = st.text_input("الشخص المسؤول:")

        if st.button("إضافة الخطة"):
            if steps.strip() == "" or responsible.strip() == "":
                st.error("جميع الحقول مطلوبة.")
            else:
                add_plan(data, selected_risk, steps, responsible)
                st.success("تم إضافة الخطة بنجاح ✔")

# ----------------------------------------
# TAB 4 : Show Plans
# ----------------------------------------
with tabs[3]:
    st.subheader("📘 كل خطط الطوارئ")

    if len(data["plans"]) == 0:
        st.info("لا توجد خطط حتى الآن.")
    else:
        for p in data["plans"]:
            st.write(f"### 🛠 للخطر: {p['risk']}")
            st.write(f"- الخطوات: {p['steps']}")
            st.write(f"- المسؤول: {p['responsible']}")
            st.markdown("---")

# ----------------------------------------
# TAB 5 : Search
# ----------------------------------------
with tabs[4]:
    st.subheader("🔍 البحث عن خطر أو خطة")

    keyword = st.text_input("اكتب كلمة البحث:")

    if keyword.strip():
        st.write("### النتائج:")

        # بحث في المخاطر
        matched_risks = [
            r for r in data["risks"]
            if keyword.lower() in r["name"].lower()
        ]

        # بحث في الخطط
        matched_plans = [
            p for p in data["plans"]
            if keyword.lower() in p["risk"].lower()
        ]

        if not matched_risks and not matched_plans:
            st.warning("لا توجد نتائج مطابقة.")
        else:
            if matched_risks:
                st.write("#### المخاطر:")
                for r in matched_risks:
                    st.write("- " + r["name"])

            if matched_plans:
                st.write("#### الخطط:")
                for p in matched_plans:
                    st.write(f"- خطة تخص: {p['risk']}")

# ----------------------------------------
# TAB 6 : Review System
# ----------------------------------------
with tabs[5]:
    st.subheader("✔ مراجعة جاهزية النظام")

    total_risks = len(data["risks"])
    total_plans = len(data["plans"])

    st.write(f"عدد المخاطر: **{total_risks}**")
    st.write(f"عدد الخطط: **{total_plans}**")

    if total_risks == 0:
        st.error("⚠ لا توجد مخاطر مسجلة. النظام غير جاهز.")
    elif total_plans < total_risks:
        st.warning("⚠ يوجد مخاطر بدون خطط! الرجاء استكمال الخطط.")
    else:
        st.success("🎉 النظام جاهز بنسبة 100% لاستمرارية العمل.")
