# 💱 Currency Converter

A modern, interactive web application for real-time currency conversion built with Streamlit. Convert amounts between multiple currencies simultaneously using live exchange rates from a free public API.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.50.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Multi-Currency Conversion**: Select multiple target currencies and convert amounts simultaneously
- **Real-Time Exchange Rates**: Fetches live exchange rates from [Frankfurter.app](https://www.frankfurter.app/) API
- **Persistent User Preferences**: Browser localStorage integration to remember selected currencies across sessions
- **Clean, Intuitive UI**: Modern, user-friendly interface with clear visual feedback
- **Smart Caching**: Efficient API response caching to minimize network requests and improve performance
- **Error Handling**: Robust error handling with fallback mechanisms for API failures
- **Responsive Design**: Clean, centered layout optimized for various screen sizes

## 🛠️ Tech Stack

- **Frontend Framework**: [Streamlit](https://streamlit.io/) - Python-based web framework for data applications
- **HTTP Client**: `requests` - For API communication
- **API**: [Frankfurter.app](https://www.frankfurter.app/) - Free, open-source currency exchange rate API
- **Language**: Python 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cursor_py
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install streamlit>=1.28.0 requests>=2.31.0
   ```

## 💻 Usage

1. **Start the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - The app will automatically open in your default web browser
   - If not, navigate to `http://localhost:8501`

3. **Using the Currency Converter**
   - **Step 1**: Select one or more currencies you want to convert to (e.g., USD, EUR, GBP, JPY)
   - **Step 2**: Enter the amount you want to convert and select the source currency
   - **Step 3**: View the converted amounts displayed in real-time

## 🏗️ Project Structure

```
cursor_py/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 🔧 Key Implementation Details

### API Integration
- **Currency List Endpoint**: Fetches available currencies with full names
- **Exchange Rates Endpoint**: Retrieves latest rates for selected currency pairs
- **Caching Strategy**: 
  - Currency list cached for 1 hour (3600s)
  - Exchange rates cached for 5 minutes (300s)

### State Management
- **Session State**: Manages user selections within the current session
- **LocalStorage**: Persists user preferences (selected currencies, source currency) across browser sessions
- **Query Parameters**: Bridges browser localStorage with Streamlit's server-side state

### Error Handling
- Graceful fallback to common currencies if API fails
- User-friendly error messages for API failures
- Input validation for amount and currency selection

## 🌐 Supported Currencies

The application supports all currencies available through the Frankfurter.app API, including:
- USD (United States Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- AUD (Australian Dollar)
- CAD (Canadian Dollar)
- CHF (Swiss Franc)
- CNY (Chinese Renminbi Yuan)
- And 24+ more currencies

*Note: The full list of supported currencies is dynamically fetched from the API.*

## 📊 API Information

This application uses the [Frankfurter.app](https://www.frankfurter.app/) API:
- **Free**: No API key required
- **No Rate Limits**: Unlimited requests
- **Open Source**: Community-maintained service
- **Data Source**: European Central Bank reference rates
- **Update Frequency**: Daily updates around 16:00 CET

## 🎯 Features in Detail

### Persistent Preferences
Your selected currencies and source currency preference are automatically saved to browser localStorage. When you refresh the page or return later, your preferences are restored automatically.

### Smart Conversion
- Automatically excludes the source currency from conversion results to avoid redundant 1:1 conversions
- Displays exchange rates alongside converted amounts
- Shows the date of the exchange rates for transparency

### Performance Optimization
- Intelligent caching reduces API calls
- Efficient data structures for currency lookups
- Minimal re-renders with Streamlit's reactive framework

## 🔒 Privacy & Security

- **No Data Collection**: The application does not collect or store any personal data
- **Client-Side Storage**: Preferences are stored locally in your browser
- **No Authentication Required**: No user accounts or login required
- **Open Source API**: Uses a transparent, open-source API service

## 🐛 Troubleshooting

### Port Already in Use
If port 8501 is already in use, Streamlit will automatically use the next available port. Check the terminal output for the correct URL.

### API Connection Issues
If you encounter API errors:
- Check your internet connection
- Verify that [api.frankfurter.dev](https://api.frankfurter.dev) is accessible
- The app includes fallback mechanisms for common scenarios

### LocalStorage Not Working
If preferences don't persist:
- Ensure cookies/localStorage are enabled in your browser
- Try clearing browser cache and reloading
- Check browser console for any JavaScript errors

## 🚧 Future Enhancements

Potential improvements for future versions:
- Historical exchange rate charts
- Currency conversion history
- Export results to CSV/PDF
- Dark mode support
- Mobile app version
- Support for cryptocurrency conversions

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

Created as a demonstration of modern web application development using Python and Streamlit.

## 🙏 Acknowledgments

- [Frankfurter.app](https://www.frankfurter.app/) for providing free, reliable exchange rate data
- [Streamlit](https://streamlit.io/) for the excellent framework
- European Central Bank for the reference exchange rate data

## 📞 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Made with ❤️ using Python and Streamlit**
