"""
Streamlit application for Currency Converter frontend.
"""
import pandas as pd
import requests
import streamlit as st

# Constants
API_URL = "http://localhost:8000"  # FastAPI service URL


def get_exchange_rates(base_currency="USD"):
    """Fetch exchange rates from the API."""
    try:
        response = requests.get(f"{API_URL}/rates/{base_currency}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None


def convert_currency(from_currency, to_currency, amount):
    """Call the API to convert currency."""
    try:
        payload = {"from_currency": from_currency, "to_currency": to_currency, "amount": float(amount)}
        response = requests.post(f"{API_URL}/convert", json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during conversion: {e}")
        return None


def main():
    """Main Streamlit app."""
    st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

    st.title("💱 Currency Converter")
    st.write("Convert currencies using real-time exchange rates")

    # Get exchange rates for available currencies
    try:
        rates_data = get_exchange_rates()
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        st.info("Make sure the FastAPI service is running at http://localhost:8000")
        st.stop()

    if not rates_data:
        st.warning("Unable to fetch currency data. Is the API running?")
        if st.button("Retry connection"):
            st.experimental_rerun()
        st.stop()

    # Available currencies
    currencies = list(rates_data["rates"].keys())
    currencies.insert(0, rates_data["base_currency"])  # Add base currency at the beginning

    # Currency selection
    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("From Currency", currencies, index=0)
    with col2:
        # Default to EUR if available, otherwise first non-base currency
        default_to = 1 if "EUR" in currencies else min(1, len(currencies) - 1)
        to_currency = st.selectbox("To Currency", currencies, index=default_to)

    # Amount input
    amount = st.number_input("Amount", min_value=0.01, value=100.00, step=10.0)

    # Convert button
    if st.button("Convert"):
        if from_currency and to_currency and amount > 0:
            try:
                with st.spinner("Converting..."):
                    result = convert_currency(from_currency, to_currency, amount)

                    if result:
                        # Display result
                        st.success(
                            f"**{amount:.2f} {from_currency}** = **{float(result['converted_amount']):.2f} {to_currency}**"
                        )

                        # Show details in expandable section
                        with st.expander("Conversion Details"):
                            st.write(f"Exchange Rate: 1 {from_currency} = {result['exchange_rate']} {to_currency}")
                            st.write(f"Updated: {result['timestamp']}")
                    else:
                        st.error("Conversion failed. Please check your inputs and try again.")
            except Exception as e:
                st.error(f"Error: {e}")

    # Show exchange rates table
    st.subheader("Current Exchange Rates")

    # Get base currency rates
    if st.button("Refresh Rates"):
        try:
            with st.spinner("Fetching latest rates..."):
                rates_data = get_exchange_rates()
                if rates_data:
                    st.success("Rates updated successfully!")
                else:
                    st.error("Failed to update rates. Please try again.")
        except Exception as e:
            st.error(f"Error: {e}")

    # Display rates in a table
    if rates_data:
        base = rates_data["base_currency"]
        df = pd.DataFrame(
            {"Currency": list(rates_data["rates"].keys()), f"Value (per 1 {base})": list(rates_data["rates"].values())}
        )
        st.dataframe(df, use_container_width=True)

        st.caption(f"Last updated: {rates_data['timestamp']}")

    # Footer
    st.markdown("---")
    st.markdown("Data provided by [ExchangeRate-API](https://www.exchangerate-api.com/)")


if __name__ == "__main__":
    main()
