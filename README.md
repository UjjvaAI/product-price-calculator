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
      <!-- Header Section -->
      <div class="text-center mb-10">
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
          <i class="fas fa-calculator text-blue-500 mr-2"></i>
          Advanced Product Pricing Calculator
        </h1>
        <p class="text-gray-600 max-w-lg mx-auto">
          Calculate pricing, margins, taxes, and profits for your products with precision
        </p>
      </div>

      <!-- Calculator Card -->
      <div class="bg-white rounded-xl shadow-xl overflow-hidden">
        <!-- Card Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-500 p-6 text-white">
          <div class="flex items-center justify-between">
            <h2 class="text-xl font-bold">
              <i class="fas fa-box-open mr-2"></i>
              Product Details
            </h2>
            <div class="flex space-x-2">
              <button class="p-2 rounded-full bg-blue-700 hover:bg-blue-800 transition" title="Help">
                <i class="fas fa-question-circle"></i>
              </button>
              <button class="p-2 rounded-full bg-blue-700 hover:bg-blue-800 transition" title="Reset">
                <i class="fas fa-redo"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Form Section -->
        <div class="p-6">
          <!-- Error Display -->
          <div id="error-display" class="hidden"></div>

          <!-- Basic Product Info -->
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

          <!-- Pricing Info -->
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

          <!-- Tax & Discount Section -->
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

          <!-- Additional Options -->
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
                    <i class="fas fa-truck mr-1 text-blue-500"></i> Shipping Cost
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
                    <i class="fas fa-cogs mr-1 text-blue-500"></i> Operating Cost (%)
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

          <!-- Calculate Button -->
          <button id="calculateButton" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-[1.01] glow mb-6">
            <i class="fas fa-calculator mr-2"></i> Calculate Pricing
          </button>

          <!-- Results Section -->
          <div id="resultsContainer" class="hidden bg-gray-50 rounded-xl border border-gray-200 overflow-hidden">
            <!-- Results Header -->
            <div class="bg-gray-100 px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-800 flex items-center">
                <i class="fas fa-chart-bar text-blue-500 mr-2"></i>
                Calculation Results
                <span id="productNameLabel" class="ml-2 text-blue-600 font-semibold">Premium Widget</span>
              </h3>
            </div>

            <!-- Results Content -->
            <div class="p-6">
              <div id="resultsOutput" class="space-y-4"></div>

              <!-- Key Metrics Card -->
              <div id="keyMetricsCard" class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <!-- Will be populated by JavaScript -->
              </div>
            </div>

            <!-- Results Footer -->
            <div class="bg-gray 50 px-6 py-3 border-t border-gray-200 text-center text-sm text-gray-500">
              <i class="fas fa-info-circle mr-1"></i> 
              Note: Markup is based on cost price, while margin is based on selling price
            </div>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
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

    // Main calculation function
    function calculatePricing(e) {
      e.preventDefault();
      
      // Clear previous errors and results
      errorDisplayDiv.innerHTML = '';
      errorDisplayDiv.classList.add('hidden');
      resultsOutputDiv.innerHTML = '';
      resultsContainer.classList.add('hidden');
      
      // Get input values
      const productName = productNameInput.value.trim() || "Unnamed Product";
      const qty = parseFloat(quantityInput.value);
      const unitPriceBeforeTax = parseFloat(unitPriceBeforeTaxInput.value);
      const selectedGstPercentage = parseFloat(gstPercentageInput.value);
      const salesPriceMrpPerUnit = parseFloat(salesPriceMrpInput.value);
      const discountPercentage = parseFloat(discountPercentageInput.value);
      const shippingCost = parseFloat(shippingCostInput.value) || 0;
      const operatingCostPercentage = parseFloat(operatingCostInput.value) || 0;
      
      // Input validation
      const errors = [];
      
      if (!productName) errors.push("Product name is required");
      if (isNaN(qty) || qty <= 0) errors.push("Quantity must be a positive number");
      if (isNaN(unitPriceBeforeTax) || unitPriceBeforeTax < 0) errors.push("Unit price must be a non-negative number");
      if (isNaN(selectedGstPercentage) || selectedGstPercentage < 0) errors.push("Tax rate must be a non-negative number");
      if (isNaN(salesPriceMrpPerUnit) || salesPriceMrpPerUnit <= 0) errors.push("Selling price must be a positive number");
      if (isNaN(discountPercentage) || discountPercentage < 0 || discountPercentage > 100) errors.push("Discount must be between 0-100%");
      
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
                    ${errors.map(e => `<li>${e}</li>`).join('')}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        `;
        return;
      }
      
      // Calculations
      const taxRateDecimal = selectedGstPercentage / 100;
      const discountRate = discountPercentage / 100;
      
      // Cost calculations
      const subtotalBeforeTax = qty * unitPriceBeforeTax;
      const taxAmountTotal = subtotalBeforeTax * taxRateDecimal;
      const subtotalAfterTax = subtotalBeforeTax + taxAmountTotal;
      const unitPriceAfterTax = unitPriceBeforeTax * (1 + taxRateDecimal);
      
      // Discounted price calculations
      const salePriceAfterDiscount = salesPriceMrpPerUnit * (1 - discountRate);
      const totalRevenue = qty * salePriceAfterDiscount;
      
      // Profit calculations
      const costOfGoodsSold = qty * unitPriceAfterTax;
      const grossProfit = totalRevenue - costOfGoodsSold;
      const grossProfitPercentage = (grossProfit / totalRevenue) * 100;
      const markupPercentage = ((salePriceAfterDiscount - unitPriceAfterTax) / unitPriceAfterTax) * 100;
      
      // Expenses
      const operatingCostAmount = totalRevenue * (operatingCostPercentage / 100);
      const totalExpenses = operatingCostAmount + shippingCost;
      const netProfit = grossProfit - totalExpenses;
      const netProfitPercentage = (netProfit / totalRevenue) * 100;
      
      // Break-even point
      const breakEvenQty = Math.ceil((totalExpenses) / (salePriceAfterDiscount - unitPriceAfterTax));
      
      // Show results
      productNameLabel.textContent = productName;
      
      // Detailed results
      const formattedNumber = (num, isCurrency = true, decimals = 2) => {
        if (isCurrency) return `$${num.toFixed(decimals)}`;
        return `${num.toFixed(decimals)}%`;
      };
      
      const renderResultItem = (label, value, isCurrency = true, icon = 'info-circle') => {
        return `
          <div class="flex justify-between py-2 border-b border-gray-200 last:border-0">
            <div class="flex items-center text-gray-700">
              <i class="fas fa-${icon} text-blue-400 mr-2"></i>
              <span class="text-sm font-medium">${label}</span>
            </div>
            <div class="${isCurrency ? 'text-gray-900 font-medium' : 'font-medium'}">
              ${formattedNumber(value, isCurrency)}
            </div>
          </div>
        `;
      };
      
      resultsOutputDiv.innerHTML = `
        <div class="space-y-4">
          <div class="result-highlight rounded-lg p-4">
            <h4 class="font-medium text-gray-700 mb-2 flex items-center">
              <i class="fas fa-dollar-sign text-blue-500 mr-2"></i>
              Cost Breakdown
            </h4>
            ${renderResultItem('Unit Cost (before tax)', unitPriceBeforeTax)}
            ${renderResultItem('Tax Rate', selectedGstPercentage, false, 'percent')}
            ${renderResultItem('Unit Cost (after tax)', unitPriceAfterTax)}
            ${renderResultItem('Total Cost (after tax)', subtotalAfterTax)}
            ${renderResultItem('Shipping Cost', shippingCost)}
          </div>
          
          <div class="result-highlight rounded-lg p-4">
            <h4 class="font-medium text-gray-700 mb-2 flex items-center">
              <i class="fas fa-tag text-blue-500 mr-2"></i>
              Pricing Information
            </h4>
            ${renderResultItem('Original Price (MRP)', salesPriceMrpPerUnit)}
            ${renderResultItem('Discount', discountPercentage, false, 'tags')}
            ${renderResultItem('Sale Price (after discount)', salePriceAfterDiscount)}
            ${renderResultItem('Total Revenue', totalRevenue)}
          </div>
          
          <div class="result-highlight rounded-lg p-4">
            <h4 class="font-medium text-gray-700 mb-2 flex items-center">
              <i class="fas fa-chart-line text-blue-500 mr-2"></i>
              Profit Metrics
            </h4>
            ${renderResultItem('Gross Profit', grossProfit, true, 'arrow-up')}
            ${renderResultItem('Gross Margin', grossProfitPercentage, false, 'chart-pie')}
            ${renderResultItem('Markup Percentage', markupPercentage, false, 'chart-line')}
            ${renderResultItem('Operating Costs', operatingCostAmount, true, 'cogs')}
            ${renderResultItem('Total Expenses', totalExpenses, true, 'receipt')}
            ${renderResultItem('Net Profit', netProfit, true, 'hand-holding-usd')}
            ${renderResultItem('Net Margin', netProfitPercentage, false, 'chart-bar')}
          </div>
        </div>
      `;
      
      // Key metrics cards
      keyMetricsCard.innerHTML = `
        <div class="bg-blue-50 border border-blue-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-percentage text-blue-500 mr-2"></i>
            <span class="font-medium text-sm text-blue-700">Profit Margin</span>
          </div>
          <h3 class="text-2xl font-bold text-blue-800">${netProfitPercentage.toFixed(1)}%</h3>
          <p class="text-xs text-blue-600 mt-1">${formattedNumber(netProfit)} net profit</p>
        </div>
        
        <div class="bg-green-50 border border-green-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-chart-line text-green-500 mr-2"></i>
            <span class="font-medium text-sm text-green-700">Markup</span>
          </div>
          <h3 class="text-2xl font-bold text-green-800">${markupPercentage.toFixed(1)}%</h3>
          <p class="text-xs text-green-600 mt-1">on ${formattedNumber(unitPriceAfterTax)} cost</p>
        </div>
        
        <div class="bg-purple-50 border border-purple-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-bullseye text-purple-500 mr-2"></i>
            <span class="font-medium text-sm text-purple-700">Break-even</span>
          </div>
          <h3 class="text-2xl font-bold text-purple-800">${breakEvenQty}</h3>
          <p class="text-xs text-purple-600 mt-1">units to cover costs</p>
        </div>
        
        <div class="bg-orange-50 border border-orange-100 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <i class="fas fa-dollar-sign text-orange-500 mr-2"></i>
            <span class="font-medium text-sm text-orange-700">ROI per Unit</span>
          </div>
          <h3 class="text-2xl font-bold text-orange-800">${formattedNumber((salePriceAfterDiscount - unitPriceAfterTax))}</h3>
          <p class="text-xs text-orange-600 mt-1">after all expenses</p>
        </div>
      `;
      
      // Show results
      resultsContainer.classList.remove('hidden');
    }
    
    // Event listeners
    calculateButton.addEventListener('click', calculatePricing);
    
    // Initialize with first calculation
    window.addEventListener('load', function() {
      setTimeout(() => {
        calculateButton.click();
        calculateButton.classList.add('animate-pulse');
        setTimeout(() => calculateButton.classList.remove('animate-pulse'), 2000);
      }, 500);
    });
  </script>
</body>
</html>
