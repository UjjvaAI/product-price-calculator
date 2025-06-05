<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Advanced Product Calculator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    .gradient-bg {
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
    }
    .glow {
      box-shadow: 0 0 15px rgba(66, 153, 225, 0.5);
    }
    input:focus, select:focus {
      box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
    }
    .result-highlight {
      background-color: #ebf8ff;
      border-left: 4px solid #4299e1;
    }
    .animate-pulse {
      animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.8; }
    }
    .scrollbar-hide::-webkit-scrollbar {
      display: none;
    }
    .scrollbar-hide {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>
<body class="gradient-bg">
  <div class="container mx-auto px-4 py-8 md:py-12">
    <div class="max-w-3xl mx-auto">
      <div class="text-center mb-10">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
          <i class="fas fa-calculator text-blue-500 mr-2"></i>
          Advanced Product Pricing Calculator
        </h1>
        <p class="text-gray-600 max-w-lg mx-auto">
          Calculate pricing, margins, taxes, and profits for your products with precision
        </p>
      </div>

      <div class="bg-white rounded-xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-blue-500 p-6 text-white">
          <div class="flex items-center justify-between">
            <h2 class="text-xl font-bold">
              <i class="fas fa-box-open mr-2"></i>
              Product Details
            </h2>
            <div class="flex space-x-2">
              <button class="p-2 rounded-full bg-blue-700 hover:bg-blue-800 transition" title="Help (Not Implemented)">
                <i class="fas fa-question-circle"></i>
              </button>
              <button class="p-2 rounded-full bg-blue-700 hover:bg-blue-800 transition" title="Reset (Not Implemented)" onclick="if(confirm('Reset fields to default? This example does not implement reset.')) { /* TODO: Implement reset logic */ }">
                <i class="fas fa-redo"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="p-6">
          <div id="error-display" class="hidden mb-4"></div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label for="productName" class="block text-sm font-medium text-gray-700 mb-1">
                <i class="fas fa-tag mr-1 text-blue-500"></i> Product Name
              </label>
              <div class="relative">
                <input type="text" id="productName" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" placeholder="Enter product name" value="Premium Widget">
                <div class="absolute right-3 top-2.5 text-gray-400">
                  <i class="fas fa-asterisk text-xs text-red-500" title="Required field"></i>
                </div>
              </div>
            </div>

            <div>
              <label for="quantity" class="block text-sm font-medium text-gray-700 mb-1">
                <i class="fas fa-boxes mr-1 text-blue-500"></i> Quantity
              </label>
              <div class="relative">
                <input type="number" id="quantity" min="1" step="1" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" value="50">
                <div class="absolute right-3 top-2.5 text-gray-400">
                  <i class="fas fa-hashtag"></i>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label for="unitPriceBeforeTax" class="block text-sm font-medium text-gray-700 mb-1">
                <i class="fas fa-tag mr-1 text-blue-500"></i> Unit Cost (before tax)
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span class="text-gray-500 sm:text-sm">$</span>
                </div>
                <input type="number" id="unitPriceBeforeTax" min="0" step="0.01" class="pl-7 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" value="24.99">
              </div>
            </div>

            <div>
              <label for="salesPriceMrp" class="block text-sm font-medium text-gray-700 mb-1">
                <i class="fas fa-dollar-sign mr-1 text-blue-500"></i> Selling Price (MRP)
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span class="text-gray-500 sm:text-sm">$</span>
                </div>
                <input type="number" id="salesPriceMrp" min="0" step="0.01" class="pl-7 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" value="39.99">
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label for="gstPercentage" class="block text-sm font-medium text-gray-700 mb-1">
                <i class="fas fa-percent mr-1 text-blue-500"></i> Tax Rate
              </label>
              <select id="gstPercentage" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition text-gray-700">
                <option value="0">0% (Tax Exempt)</option>
                <option value="5">5%</option>
                <option value="12" selected>12%</option>
                <option value="18">18%</option>
                <option value="28">28%</option>
              </select>
            </div>

            <div>
              <label for="discountPercentage" class="block text-sm font-medium text-gray-700 mb-1">
                <i class="fas fa-tags mr-1 text-blue-500"></i> Discount (%)
              </label>
              <div class="relative">
                <input type="number" id="discountPercentage" min="0" max="100" step="0.5" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" value="10">
                <div class="absolute right-3 top-2.5 text-gray-400">
                  <i class="fas fa-percent"></i>
                </div>
              </div>
            </div>
          </div>

          <div class="mb-6">
            <div class="flex items-center">
              <input type="checkbox" id="showAdvanced" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
              <label for="showAdvanced" class="ml-2 block text-sm text-gray-700">
                Show advanced options
              </label>
            </div>
            <div id="advancedOptions" class="hidden mt-4 space-y-4 border-t pt-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="shippingCost" class="block text-sm font-medium text-gray-700 mb-1">
                    <i class="fas fa-truck mr-1 text-blue-500"></i> Shipping Cost (Total)
                  </label>
                  <div class="relative">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <span class="text-gray-500 sm:text-sm">$</span>
                    </div>
                    <input type="number" id="shippingCost" min="0" step="0.01" class="pl-7 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" value="5.99">
                  </div>
                </div>
                <div>
                  <label for="operatingCost" class="block text-sm font-medium text-gray-700 mb-1">
                    <i class="fas fa-cogs mr-1 text-blue-500"></i> Operating Cost (% of Revenue)
                  </label>
                  <div class="relative">
                    <input type="number" id="operatingCost" min="0" max="100" step="0.1" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 transition" value="12">
                    <div class="absolute right-3 top-2.5 text-gray-400">
                      <i class="fas fa-percent"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button id="calculateButton" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-[1.01] glow mb-6">
            <i class="fas fa-calculator mr-2"></i> Calculate Pricing
          </button>

          <div id="resultsContainer" class="hidden bg-gray-50 rounded-xl border border-gray-200 overflow-hidden">
            <div class="bg-gray-100 px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-800 flex items-center">
                <i class="fas fa-chart-bar text-blue-500 mr-2"></i>
                Calculation Results for:
                <span id="productNameLabel" class="ml-2 text-blue-600 font-semibold">Premium Widget</span>
              </h3>
            </div>

            <div class="p-6">
              <div id="resultsOutput" class="space-y-4"></div>

              <div id="keyMetricsCard" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                </div>
            </div>

            <div class="bg-gray-50 px-6 py-3 border-t border-gray-200 text-center text-sm text-gray-500">
              <i class="fas fa-info-circle mr-1"></i>
              Note: Markup is based on cost price, while margin is based on selling price.
            </div>
          </div>
        </div>
      </div>

      <div class="mt-6 text-center text-xs text-gray-400">
        <p>This calculator is for informational purposes only. Actual prices may vary based on market conditions.</p>
      </div>
    </div>
  </div>

  <script>
    // DOM Elements
    const productNameInput = document.getElementById('productName');
    const quantityInput = document.getElementById('quantity');
    const unitPriceBeforeTaxInput = document.getElementById('unitPriceBeforeTax');
    const gstPercentageInput = document.getElementById('gstPercentage');
    const salesPriceMrpInput = document.getElementById('salesPriceMrp');
    const discountPercentageInput = document.getElementById('discountPercentage');
    const shippingCostInput = document.getElementById('shippingCost');
    const operatingCostInput = document.getElementById('operatingCost');
    const showAdvancedCheckbox = document.getElementById('showAdvanced');
    const advancedOptionsDiv = document.getElementById('advancedOptions');
    const calculateButton = document.getElementById('calculateButton');
    const errorDisplayDiv = document.getElementById('error-display');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsOutputDiv = document.getElementById('resultsOutput');
    const keyMetricsCard = document.getElementById('keyMetricsCard');
    const productNameLabel = document.getElementById('productNameLabel');

    // Toggle advanced options
    showAdvancedCheckbox.addEventListener('change', function() {
      advancedOptionsDiv.classList.toggle('hidden', !this.checked);
    });

    // Helper function for formatting numbers
    const formatOutput = (num, type = 'currency', decimals = 2) => {
        if (type === 'percentage' && num === Infinity) return "Infinite %";
        if (type === 'qty' && num === Infinity) return "Cannot calculate"; // For break-even

        if (isNaN(num) || !isFinite(num)) {
            if (type === 'currency') return "$N/A";
            if (type === 'percentage') return "N/A %";
            if (type === 'qty') return "N/A";
            return "N/A";
        }

        if (type === 'currency') return `$${num.toFixed(decimals)}`;
        if (type === 'percentage') return `${num.toFixed(decimals)}%`;
        if (type === 'qty') return Math.ceil(num).toString(); // Typically for whole units
        return num.toFixed(decimals); // Generic number formatting
    };


    // Main calculation function
    function calculatePricing(e) {
      if (e) e.preventDefault(); // Allow calling without event

      // Clear previous errors and results
      errorDisplayDiv.innerHTML = '';
      errorDisplayDiv.classList.add('hidden');
      // resultsOutputDiv.innerHTML = ''; // Cleared later by population
      // keyMetricsCard.innerHTML = ''; // Cleared later by population
      // resultsContainer.classList.add('hidden'); // Shown at the end

      // Get input values
      const productName = productNameInput.value.trim() || "Unnamed Product";
      const qty = parseFloat(quantityInput.value);
      const unitPriceBeforeTax = parseFloat(unitPriceBeforeTaxInput.value);
      const selectedGstPercentage = parseFloat(gstPercentageInput.value);
      const salesPriceMrpPerUnit = parseFloat(salesPriceMrpInput.value);
      const discountPercentage = parseFloat(discountPercentageInput.value);
      
      let shippingCost = 0;
      let operatingCostPercentage = 0;
      if (showAdvancedCheckbox.checked) {
          shippingCost = parseFloat(shippingCostInput.value) || 0;
          operatingCostPercentage = parseFloat(operatingCostInput.value) || 0;
      }
      
      // Input validation
      const errors = [];
      if (!productNameInput.value.trim()) errors.push("Product name is required");
      if (isNaN(qty) || qty <= 0) errors.push("Quantity must be a positive number");
      if (isNaN(unitPriceBeforeTax) || unitPriceBeforeTax < 0) errors.push("Unit cost must be a non-negative number");
      if (isNaN(selectedGstPercentage) || selectedGstPercentage < 0) errors.push("Tax rate must be a non-negative number");
      if (isNaN(salesPriceMrpPerUnit) || salesPriceMrpPerUnit <= 0) errors.push("Selling price must be a positive number");
      if (isNaN(discountPercentage) || discountPercentage < 0 || discountPercentage > 100) errors.push("Discount must be between 0-100%");
      if (showAdvancedCheckbox.checked) {
        if (isNaN(shippingCost) || shippingCost < 0) errors.push("Shipping cost must be a non-negative number.");
        if (isNaN(operatingCostPercentage) || operatingCostPercentage < 0 || operatingCostPercentage > 100) errors.push("Operating cost must be between 0-100%.");
      }


      if (errors.length > 0) {
        errorDisplayDiv.classList.remove('hidden');
        errorDisplayDiv.innerHTML = `
          <div class="bg-red-50 border-l-4 border-red-400 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <i class="fas fa-exclamation-circle text-red-400"></i>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">Please correct the following errors:</h3>
                <div class="mt-2 text-sm text-red-700">
                  <ul class="list-disc pl-5 space-y-1">
                    ${errors.map(err => `<li>${err}</li>`).join('')}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        `;
        resultsContainer.classList.add('hidden');
        return;
      }
      
      // Calculations
      const taxRateDecimal = selectedGstPercentage / 100;
      const discountRate = discountPercentage / 100;
      
      const unitPriceAfterTax = unitPriceBeforeTax * (1 + taxRateDecimal);
      const subtotalAfterTax = qty * unitPriceAfterTax; // Total cost of goods for the quantity

      const salePriceAfterDiscount = salesPriceMrpPerUnit * (1 - discountRate);
      const totalRevenue = qty * salePriceAfterDiscount;
      
      const costOfGoodsSold = unitPriceAfterTax * qty; // Same as subtotalAfterTax
      const grossProfit = totalRevenue - costOfGoodsSold;
      
      const grossProfitPercentage = totalRevenue !== 0 ? (grossProfit / totalRevenue) * 100 : 0;
      const markupPercentage = unitPriceAfterTax !== 0 ? ((salePriceAfterDiscount - unitPriceAfterTax) / unitPriceAfterTax) * 100 : Infinity;
      
      const operatingCostAmount = totalRevenue * (operatingCostPercentage / 100);
      const totalFixedExpenses = shippingCost; // Assuming shipping is the main fixed expense for this batch calculation
      const totalVariableExpensesNotCOGS = operatingCostAmount;
      const totalExpenses = totalVariableExpensesNotCOGS + totalFixedExpenses;

      const netProfit = grossProfit - totalExpenses;
      const netProfitPercentage = totalRevenue !== 0 ? (netProfit / totalRevenue) * 100 : 0;
      
      // Break-even point
      let breakEvenQty;
      // Variable cost per unit = unit cost after tax + (selling price per unit * operating cost percentage)
      const effectiveUnitVariableCost = unitPriceAfterTax + (salePriceAfterDiscount * (operatingCostPercentage / 100));
      // Contribution margin per unit = selling price - all variable costs per unit
      const unitContributionToFixedCosts = salePriceAfterDiscount - effectiveUnitVariableCost;

      if (unitContributionToFixedCosts <= 0) {
          breakEvenQty = (totalFixedExpenses > 0) ? Infinity : 0; 
      } else {
          breakEvenQty = totalFixedExpenses / unitContributionToFixedCosts; // No Math.ceil here, formatOutput will handle
      }
      
      // Show results
      productNameLabel.textContent = productName;
      
      const renderResultItem = (label, value, type = 'currency', icon = 'info-circle', decimals = 2) => {
        return `
          <div class="flex justify-between py-2 border-b border-gray-200 last:border-0">
            <div class="flex items-center text-gray-700">
              <i class="fas fa-${icon} text-blue-400 mr-2"></i>
              <span class="text-sm font-medium">${label}</span>
            </div>
            <div class="text-gray-900 font-medium">
              ${formatOutput(value, type, decimals)}
            </div>
          </div>
        `;
      };
      
      resultsOutputDiv.innerHTML = `
        <div class="space-y-4">
          <div class="result-highlight rounded-lg p-4">
            <h4 class="font-medium text-gray-700 mb-2 flex items-center">
              <i class="fas fa-dollar-sign text-blue-500 mr-2"></i> Cost Breakdown
            </h4>
            ${renderResultItem('Unit Cost (before tax)', unitPriceBeforeTax, 'currency', 'file-invoice-dollar')}
            ${renderResultItem('Tax Rate', selectedGstPercentage, 'percentage', 'percentage', 2)}
            ${renderResultItem('Unit Cost (after tax)', unitPriceAfterTax, 'currency', 'money-check-alt')}
            ${renderResultItem(`Total Cost for ${qty} Units (after tax)`, subtotalAfterTax, 'currency', 'cart-plus')}
            ${showAdvancedCheckbox.checked ? renderResultItem('Shipping Cost (Total Fixed)', shippingCost, 'currency', 'truck') : ''}
          </div>
          
          <div class="result-highlight rounded-lg p-4">
            <h4 class="font-medium text-gray-700 mb-2 flex items-center">
              <i class="fas fa-tag text-blue-500 mr-2"></i> Pricing & Revenue
            </h4>
            ${renderResultItem('Original Price (MRP per unit)', salesPriceMrpPerUnit, 'currency', 'tag')}
            ${renderResultItem('Discount', discountPercentage, 'percentage', 'tags', 2)}
            ${renderResultItem('Sale Price (per unit, after discount)', salePriceAfterDiscount, 'currency', 'cash-register')}
            ${renderResultItem(`Total Revenue for ${qty} Units`, totalRevenue, 'currency', 'coins')}
          </div>
          
          <div class="result-highlight rounded-lg p-4">
            <h4 class="font-medium text-gray-700 mb-2 flex items-center">
              <i class="fas fa-chart-line text-blue-500 mr-2"></i> Profit Metrics
            </h4>
            ${renderResultItem('Gross Profit', grossProfit, 'currency', 'arrow-up')}
            ${renderResultItem('Gross Margin', grossProfitPercentage, 'percentage', 'chart-pie', 2)}
            ${renderResultItem('Markup Percentage (on unit cost)', markupPercentage, 'percentage', 'chart-line', 2)}
            ${showAdvancedCheckbox.checked ? renderResultItem('Operating Costs (Total)', operatingCostAmount, 'currency', 'cogs') : ''}
            ${showAdvancedCheckbox.checked ? renderResultItem('Total Additional Expenses', totalExpenses, 'currency', 'receipt') : ''}
            ${renderResultItem('Net Profit', netProfit, 'currency', 'hand-holding-usd')}
            ${renderResultItem('Net Margin', netProfitPercentage, 'percentage', 'chart-bar', 2)}
          </div>
        </div>
      `;
      
      const unitGrossProfit = salePriceAfterDiscount - unitPriceAfterTax;

      keyMetricsCard.innerHTML = `
        <div class="bg-blue-50 border border-blue-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-percentage text-blue-500 mr-2"></i>
            <span class="font-medium text-sm text-blue-700">Net Profit Margin</span>
          </div>
          <h3 class="text-2xl font-bold text-blue-800">${formatOutput(netProfitPercentage, 'percentage', 1)}</h3>
          <p class="text-xs text-blue-600 mt-1">${formatOutput(netProfit, 'currency')} net profit total</p>
        </div>
        
        <div class="bg-green-50 border border-green-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-chart-line text-green-500 mr-2"></i>
            <span class="font-medium text-sm text-green-700">Markup %</span>
          </div>
          <h3 class="text-2xl font-bold text-green-800">${formatOutput(markupPercentage, 'percentage', 1)}</h3>
          <p class="text-xs text-green-600 mt-1">on ${formatOutput(unitPriceAfterTax, 'currency')} unit cost</p>
        </div>
        
        <div class="bg-purple-50 border border-purple-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-bullseye text-purple-500 mr-2"></i>
            <span class="font-medium text-sm text-purple-700">Break-even Units</span>
          </div>
          <h3 class="text-2xl font-bold text-purple-800">${formatOutput(breakEvenQty, 'qty', 0)}</h3>
          <p class="text-xs text-purple-600 mt-1">units to cover fixed costs</p>
        </div>
        
        <div class="bg-orange-50 border border-orange-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-dollar-sign text-orange-500 mr-2"></i>
            <span class="font-medium text-sm text-orange-700">Unit Gross Profit</span>
          </div>
          <h3 class="text-2xl font-bold text-orange-800">${formatOutput(unitGrossProfit, 'currency')}</h3>
          <p class="text-xs text-orange-600 mt-1">before op. & shipping costs</p>
        </div>
      `;
      
      resultsContainer.classList.remove('hidden');
    }
    
    // Event listeners
    calculateButton.addEventListener('click', calculatePricing);
    
    // Initialize with first calculation on load
    window.addEventListener('load', function() {
      setTimeout(() => {
        // Ensure advanced options defaults are set if checkbox is not checked
        if (!showAdvancedCheckbox.checked) {
            shippingCostInput.value = "0"; // Or your desired default when hidden
            operatingCostInput.value = "0"; // Or your desired default when hidden
        }
        calculatePricing(); // Call without event object
        calculateButton.classList.add('animate-pulse');
        setTimeout(() => calculateButton.classList.remove('animate-pulse'), 2000);
      }, 100); // Reduced timeout for quicker load
    });
  </script>
</body>
</html>
