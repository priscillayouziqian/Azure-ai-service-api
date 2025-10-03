import streamlit as st


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def compute_bmi(weight_kg: float, height_m: float) -> float:
	"""Compute BMI given weight in kg and height in meters."""
	if height_m <= 0:
		raise ValueError("Height must be greater than zero")
	return weight_kg / (height_m ** 2)


def classify_bmi(bmi: float) -> str:
	"""Return BMI category name for a BMI value.

	This maps the numeric BMI into standard categories.
	"""
	if bmi < 18.5:
		return "Underweight"
	if bmi < 25:
		return "Normal weight"
	if bmi < 30:
		return "Overweight"
	return "Obese"


# ---------------------------------------------------------------------------
# App layout and logic
# ---------------------------------------------------------------------------
def main() -> None:
	st.set_page_config(page_title="Week 7 — BMI Calculator", page_icon="⚖️")
	st.title("BMI Calculator 🎯")
	st.write("Enter your weight and height to compute your Body Mass Index (BMI).")

	# Use two columns to lay out weight and height controls side-by-side
	col1, col2 = st.columns(2)

	with col1:
		# input in kg (decimal) in positive decimal values
		weight = st.number_input("Weight (kg)", min_value=0.1, value=70.0, step=0.1, format="%.1f")

	with col2:
		# input choose m/cm via radio button
		unit = st.radio("Height unit", options=["meters", "centimeters"], index=0, horizontal=True)
		if unit == "meters":
			# input in meters (decimal)
			height_input = st.number_input("Height (m)", min_value=0.5, value=1.70, step=0.01, format="%.2f")
			height_m = float(height_input)
		else:
			# input in centimeters (integer-like)
			height_cm = st.number_input("Height (cm)", min_value=50.0, value=170.0, step=1.0, format="%.0f")
			# convert cm to m for easy calculation
			height_m = float(height_cm) / 100.0

	# --------------------------------------------------------------------------
    # Below is result display, only BMI button click triggers display results
	# --------------------------------------------------------------------------
	
	# st.button returns false by default, and True only on the run where user clicks
	compute = st.button("Calculate BMI")

	if compute:
		try:
			bmi = compute_bmi(weight, height_m)
		except Exception as e:
			st.error(f"Error computing BMI: {e}")
			return

        # BMI value rounded to 1 decimal place
		bmi_display = round(bmi, 1)
		category = classify_bmi(bmi)

		# Show results: a metric (big numeric display) and a category label
		st.subheader("Result")
		cols = st.columns([1, 2], border=True) # create two columns with ratio 1:2
		cols[0].metric("BMI", f"{bmi_display}")
		# Make the category visually prominent using Streamlit's message widgets
		cols[1].write("Category:")
		if category == "Underweight":
			cols[1].info(f"🔵 {category}")
			cols[1].info("Consider consulting a healthcare professional for personalized advice.")
		elif category == "Normal weight":
			cols[1].success(f"✅ {category}")
			cols[1].success("keep up the healthy habits!")
		elif category == "Overweight":
			cols[1].warning(f"⚠️ {category}")
			cols[1].warning("Consider lifestyle changes like balanced diet and regular exercise.")
		else:
			cols[1].error(f"⛔ {category}")
			cols[1].error("It's advisable to consult with a healthcare professional.")

		


if __name__ == "__main__":
	main()

