import streamlit as st
import requests
from typing import Dict, List, Optional

# Page config
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered"
)

# API Configuration
API_BASE_URL = "https://api.frankfurter.dev/v1"


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_currencies() -> Dict[str, str]:
    """Fetch available currencies from Frankfurter API."""
    try:
        response = requests.get(f"{API_BASE_URL}/currencies", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch currencies: {e}")
        # Fallback to common currencies
        return {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "AUD": "Australian Dollar",
            "CAD": "Canadian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Renminbi Yuan",
        }


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_latest_rates(base_currency: str, target_currencies: List[str]) -> Optional[Dict]:
    """Fetch latest exchange rates from Frankfurter API."""
    if not target_currencies:
        return None
    
    try:
        symbols = ",".join(target_currencies)
        url = f"{API_BASE_URL}/latest"
        params = {"base": base_currency, "symbols": symbols}
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch exchange rates: {e}")
        return None


def create_local_storage_sync_component():
    """Create a component that syncs Streamlit session_state with browser localStorage.
    Handles both loading from localStorage (on first visit) and saving to localStorage (on changes).
    """
    import json
    
    # Get current values from session_state
    selected_currencies = st.session_state.get("selected_currencies", [])
    source_currency = st.session_state.get("source_currency", "USD")
    
    # Check if we've already loaded from localStorage
    has_loaded = st.session_state.get("localStorage_initialized", False)
    
    script = f"""
    <script>
    (function() {{
        const hasLoaded = {str(has_loaded).lower()};
        const urlParams = new URLSearchParams(window.location.search);
        const hasQueryParams = urlParams.has('currencies') || urlParams.has('source_currency');
        
        // Phase 1: Load from localStorage on first visit (only if not already loaded)
        if (!hasLoaded && !hasQueryParams) {{
            const savedCurrencies = localStorage.getItem('selected_currencies');
            const savedSource = localStorage.getItem('source_currency');
            
            if (savedCurrencies || savedSource) {{
                const params = new URLSearchParams();
                if (savedCurrencies) {{
                    params.set('currencies', savedCurrencies);
                }}
                if (savedSource) {{
                    params.set('source_currency', savedSource);
                }}
                // Update URL and reload to let Streamlit read query params
                window.location.search = params.toString();
                return;
            }}
        }}
        
        // Phase 2: Save current values to localStorage (runs on every rerun after initialization)
        // Only save if we've initialized (to avoid overwriting with empty values on first load)
        if (hasLoaded || hasQueryParams) {{
            const currentCurrencies = {json.dumps(selected_currencies)};
            const currentSource = '{source_currency}';
            
            if (Array.isArray(currentCurrencies)) {{
                localStorage.setItem('selected_currencies', JSON.stringify(currentCurrencies));
            }}
            
            if (currentSource) {{
                localStorage.setItem('source_currency', currentSource);
            }}
        }}
    }})();
    </script>
    """
    st.components.v1.html(script, height=0)


def main():
    st.title("💱 Currency Converter")
    st.markdown("Convert amounts between currencies using live exchange rates")
    
    # Initialize session state for persistence
    # Try to load from query params (which are set by localStorage script on first visit)
    query_params = st.query_params
    
    # Check if this is the initial load (no session state initialized yet)
    is_initial_load = "selected_currencies" not in st.session_state
    
    # Load selected currencies from query params (set by localStorage on first visit)
    if is_initial_load:
        if "currencies" in query_params:
            try:
                import json
                currencies_str = query_params["currencies"]
                # Handle both string and list formats
                if isinstance(currencies_str, str):
                    st.session_state.selected_currencies = json.loads(currencies_str)
                elif isinstance(currencies_str, list):
                    st.session_state.selected_currencies = currencies_str
                else:
                    st.session_state.selected_currencies = []
            except Exception as e:
                st.session_state.selected_currencies = []
        else:
            st.session_state.selected_currencies = []
    
    # Load source currency from query params
    if is_initial_load:
        if "source_currency" in query_params:
            st.session_state.source_currency = query_params["source_currency"]
        else:
            st.session_state.source_currency = "USD"
    
    # Initialize localStorage sync component (handles both loading and saving)
    # Only save to localStorage if we've completed initial load (to avoid overwriting with empty values)
    if not is_initial_load:
        create_local_storage_sync_component()
    else:
        # On initial load, create component that will load from localStorage if needed
        create_local_storage_sync_component()
        # Mark as initialized after first load attempt
        st.session_state.localStorage_initialized = True
    
    # Fetch available currencies
    currencies = fetch_currencies()
    currency_codes = sorted(currencies.keys())
    currency_options = {code: f"{code} - {currencies[code]}" for code in currency_codes}
    
    st.divider()
    
    # Step 1: Select currencies of interest
    st.subheader("Step 1: Select Currencies")
    selected_currency_labels = st.multiselect(
        "Choose currencies to convert to:",
        options=list(currency_options.values()),
        default=[currency_options.get(code, code) for code in st.session_state.selected_currencies 
                 if code in currency_options],
        key="currency_multiselect"
    )
    
    # Extract currency codes from selected labels
    selected_currencies = [
        code for code, label in currency_options.items() 
        if label in selected_currency_labels
    ]
    
    # Save to session state (localStorage sync happens in create_local_storage_sync_component)
    st.session_state.selected_currencies = selected_currencies
    
    st.divider()
    
    # Step 2: Enter amount and select source currency
    st.subheader("Step 2: Enter Amount & Source Currency")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input(
            "Amount:",
            min_value=0.0,
            value=100.0,
            step=0.01,
            format="%.2f"
        )
    
    with col2:
        source_currency = st.selectbox(
            "From Currency:",
            options=currency_codes,
            index=currency_codes.index(st.session_state.source_currency) if st.session_state.source_currency in currency_codes else 0,
            format_func=lambda x: f"{x} - {currencies[x]}"
        )
        st.session_state.source_currency = source_currency
    # localStorage sync happens in create_local_storage_sync_component
    
    st.divider()
    
    # Step 3: Convert and display results
    st.subheader("Step 3: Conversion Results")
    
    if not selected_currencies:
        st.info("👆 Please select at least one currency to convert to.")
    elif source_currency in selected_currencies:
        st.warning(f"⚠️ Source currency ({source_currency}) is in your selected currencies. It will show as 1:1 conversion.")
    
    if selected_currencies and amount > 0:
        # Remove source currency from target list to avoid showing 1:1 conversion
        target_currencies = [c for c in selected_currencies if c != source_currency]
        
        if target_currencies:
            with st.spinner("Fetching latest exchange rates..."):
                rates_data = fetch_latest_rates(source_currency, target_currencies)
            
            if rates_data:
                rates = rates_data.get("rates", {})
                rate_date = rates_data.get("date", "N/A")
                
                st.success(f"✅ Exchange rates updated as of {rate_date}")
                st.caption(f"Rates from [Frankfurter.app](https://www.frankfurter.app/)")
                
                # Display results in a clean format
                st.markdown("### Converted Amounts:")
                
                # Create columns for better layout
                num_cols = 2
                cols = st.columns(num_cols)
                
                for idx, currency in enumerate(target_currencies):
                    rate = rates.get(currency, 0)
                    converted_amount = amount * rate
                    
                    with cols[idx % num_cols]:
                        st.metric(
                            label=f"{amount:,.2f} {source_currency} → {currency}",
                            value=f"{converted_amount:,.2f}",
                            delta=f"Rate: {rate:.4f}" if rate else None
                        )
                
                # Also show source currency if it was selected
                if source_currency in selected_currencies:
                    with cols[0]:
                        st.metric(
                            label=f"{amount:,.2f} {source_currency} → {source_currency}",
                            value=f"{amount:,.2f}",
                            delta="Same currency"
                        )
            else:
                st.error("Unable to fetch exchange rates. Please try again later.")
        else:
            st.info("All selected currencies are the same as the source currency. Please select different currencies to convert to.")


if __name__ == "__main__":
    main()
