# Quick Start Guide - R Portfolio Analysis

## ⚡ Get Started in 2 Steps

### Step 1: Install Packages (One-time setup)
Open R or RStudio and run:

```r
setwd("c:/Users/dorma/OneDrive/Repos/Empirical_RA/R_version")
source("setup.R")
```

**Expected time:** 2-5 minutes (depending on internet speed)

### Step 2: Run Analysis
```r
source("portfolio_analysis.R")
```

**Expected time:** 2-3 minutes (data download + calculations)

---

## 📊 What to Expect

The script will:
1. ✅ Download 10 years of data for Pfizer, JPY/PLN, Gold (+ benchmark)
2. ✅ Calculate all risk metrics (VaR, CVaR, Sharpe, Beta, etc.) 
3. ✅ Display 9 interactive plots (press Enter between each)
4. ✅ Print comprehensive summary to console

**No files are created** - everything displays in console/plots panel.

---

## 🎯 Quick Reference

### Calculations Included
- Mean returns (daily, monthly, yearly)
- Standard deviation / volatility
- Correlation & covariance matrices
- VaR (Historical, Parametric, Monte Carlo)
- CVaR / Expected Shortfall
- Sharpe Ratio
- Beta & Alpha vs MSCI World

### Visualizations
1. Asset prices rebased to 100
2. Return distribution histograms  
3. Correlation heatmap
4. Rolling 20-day volatility
5-7. VaR breach analysis (3 methods)
8. CVaR breach analysis
9. Beta regression scatter plot

---

## 🔧 Troubleshooting

### Problem: Package installation fails
**Solution:** Install Rtools (Windows only)
- Download: https://cran.r-project.org/bin/windows/Rtools/

### Problem: Yahoo Finance data not loading
**Solution:** Check internet connection or try shorter time period
```r
# Edit portfolio_analysis.R, line 300:
start_date <- end_date - (8 * 365)  # Use 8 years instead of 10
```

### Problem: Plots not showing
**Solution (RStudio):** Go to Plots pane → Click "Zoom" 
**Solution (R GUI):** Graphics window should open automatically

### Problem: "URTH not found" warning
**Solution:** This is normal - script continues without benchmark data

---

## 📝 Example Output

After running, you'll see:

```
================================================================================
STARTING FULL PORTFOLIO ANALYSIS - R IMPLEMENTATION
================================================================================

[STEP 1] Loading data from Yahoo Finance...
  Loading data for Pfizer (PFE)...
    Fetching FX data: USDPLN=X...
    [OK] Pfizer: 2523 data points
  Loading data for JPY/PLN (JPYPLN=X)...
    [OK] JPY/PLN: 2619 data points
  Loading data for Gold (GC=F)...
    Fetching FX data: USDPLN=X...
    [OK] Gold: 2546 data points
[OK] Portfolio created with 3 assets
[OK] Data loaded: 2516 dates, 3 assets

[STEP 2] Calculating returns...
[OK] Returns calculated: 2515 observations
[OK] Portfolio returns calculated: 2515 observations

[STEP 3] Analyzing returns...
[OK] Mean daily returns: 0.000423
[OK] Mean yearly returns: 0.1066

...

[STEP 9] Generating visualizations...
[PLOT 1] Price timeseries rebased to 100...
Press [Enter] to continue to next plot...
```

---

## 🎓 Academic Use

This implementation satisfies the requirements for:
- **Course:** Empirical Methods of Risk Assessment
- **Portfolio:** 50% Pfizer, 25% JPY/PLN, 25% Gold
- **Value:** 100,000 PLN
- **Methods:** All required calculations (VaR, CVaR, Sharpe, Beta, etc.)

**Key Differences from Python:**
- ✅ Same calculations, different implementation
- ✅ Uses established R finance packages
- ✅ More concise code (~450 lines vs ~700)
- ❌ No file exports (console/plots only)

---

## 💡 Tips for Best Experience

### In RStudio (Recommended)
1. **Console:** Bottom-left (shows progress messages)
2. **Plots:** Bottom-right (shows visualizations)
3. **Zoom plots:** Click "Zoom" button for full-size view
4. **Navigate:** Use arrow buttons to review previous plots

### In R GUI
1. Graphics windows open automatically
2. Press Enter in console to advance
3. Keep console window focused

### Save Results (Optional)
While the script doesn't export files, you can:
- Copy console output → Save as .txt
- Right-click plots → "Save Image As"
- Or modify script to add `ggsave()` calls

---

## 📞 Need Help?

**Common Questions:**

**Q: How long does it take?**  
A: ~5 minutes total (3 min setup + 2 min analysis)

**Q: Can I change the portfolio?**  
A: Yes! Edit lines 289-291 in `portfolio_analysis.R`:
```r
WEIGHTS <- c(0.50, 0.25, 0.25)  # Modify these percentages
```

**Q: Can I export results to CSV?**  
A: Not included per requirements, but you can add:
```r
# After Step 10, add:
write.csv(as.data.frame(returns_df), "returns.csv")
```

**Q: How accurate is this vs Python?**  
A: Differences < 0.1% due to numerical precision. Both methods are valid.

---

## ✅ Ready to Start?

```r
# 1. Install packages (one time)
source("setup.R")

# 2. Run analysis
source("portfolio_analysis.R")

# 3. View results in console + plots pane
```

**That's it! Enjoy your portfolio analysis! 📈**
