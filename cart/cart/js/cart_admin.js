document.addEventListener("DOMContentLoaded", function () {

    const inlineGroup = document.querySelector("#cartitem_set-group");

    if (!inlineGroup) {
        return;
    }

    function getRows() {
        return inlineGroup.querySelectorAll(
            "tbody tr.form-row"
        );
    }

    function updateCartTotal() {

        let totalItems = 0;
        let totalPrice = 0;

        getRows().forEach(function (row) {

            if (
                row.classList.contains("empty-form") ||
                row.style.display === "none"
            ) {
                return;
            }

            const quantityInput =
                row.querySelector(
                    'input[name$="-quantity"]'
                );

            if (!quantityInput) {
                return;
            }

            const quantity =
                parseInt(quantityInput.value) || 0;

            const unitPriceElement =
                row.querySelector(".field-unit_price");

            if (!unitPriceElement) {
                return;
            }

            const priceText =
                unitPriceElement.innerText
                    .replace(/[₹,]/g, "")
                    .trim();

            const unitPrice =
                parseFloat(priceText) || 0;

            totalItems += quantity;
            totalPrice += quantity * unitPrice;
        });

        const totalItemsElement =
            document.querySelector(
                "#id_display_total_items"
            );

        const totalPriceElement =
            document.querySelector(
                "#id_display_total_price"
            );

        if (totalItemsElement) {
            totalItemsElement.innerText =
                totalItems;
        }

        if (totalPriceElement) {
            totalPriceElement.innerText =
                "₹ " +
                totalPrice.toLocaleString("en-IN", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
        }

        let cartSummary =
            document.querySelector(".live-cart-summary");

        if (!cartSummary) {

            cartSummary =
                document.createElement("div");

            cartSummary.className =
                "live-cart-summary";

            inlineGroup.parentNode.insertBefore(
                cartSummary,
                inlineGroup
            );
        }

        cartSummary.innerHTML = `
            <div class="cart-summary-item">
                <span>🛒 Items</span>
                <strong>${totalItems}</strong>
            </div>

            <div class="cart-summary-item">
                <span>💰 Cart Total</span>
                <strong>₹ ${totalPrice.toLocaleString(
                    "en-IN",
                    {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }
                )}</strong>
            </div>
        `;
    }


    function addQuantityControls(row) {

        const quantityInput =
            row.querySelector(
                'input[name$="-quantity"]'
            );

        if (!quantityInput) {
            return;
        }

        if (
            quantityInput.parentElement
                .classList.contains("quantity-control")
        ) {
            return;
        }

        const wrapper =
            document.createElement("div");

        wrapper.className =
            "quantity-control";

        const minus =
            document.createElement("button");

        minus.type = "button";
        minus.className =
            "quantity-btn quantity-minus";

        minus.innerHTML = "−";

        const plus =
            document.createElement("button");

        plus.type = "button";
        plus.className =
            "quantity-btn quantity-plus";

        plus.innerHTML = "+";

        quantityInput.parentNode.insertBefore(
            wrapper,
            quantityInput
        );

        wrapper.appendChild(minus);
        wrapper.appendChild(quantityInput);
        wrapper.appendChild(plus);

        minus.addEventListener(
            "click",
            function () {

                let value =
                    parseInt(quantityInput.value) || 1;

                if (value > 1) {
                    value--;
                    quantityInput.value = value;
                    updateCartTotal();
                }
            }
        );

        plus.addEventListener(
            "click",
            function () {

                let value =
                    parseInt(quantityInput.value) || 0;

                value++;

                quantityInput.value = value;

                updateCartTotal();
            }
        );

        quantityInput.addEventListener(
            "input",
            function () {

                if (
                    quantityInput.value < 1
                ) {
                    quantityInput.value = 1;
                }

                updateCartTotal();
            }
        );
    }


    function addRemoveButton(row) {

        if (
            row.classList.contains("empty-form")
        ) {
            return;
        }

        if (
            row.querySelector(".custom-remove-btn")
        ) {
            return;
        }

        const deleteCheckbox =
            row.querySelector(
                'input[name$="-DELETE"]'
            );

        if (!deleteCheckbox) {
            return;
        }

        const button =
            document.createElement("button");

        button.type = "button";

        button.className =
            "custom-remove-btn";

        button.innerHTML =
            "🗑 Remove";

        deleteCheckbox.style.display =
            "none";

        deleteCheckbox.parentElement
            .style.display = "none";

        button.addEventListener(
            "click",
            function () {

                deleteCheckbox.checked = true;

                row.style.display = "none";

                updateCartTotal();
            }
        );

        const removeCell =
            row.querySelector(".field-remove_item");

        if (removeCell) {

            removeCell.innerHTML = "";

            removeCell.appendChild(button);
        }
    }


    function initializeRows() {

        getRows().forEach(function (row) {

            addQuantityControls(row);
            addRemoveButton(row);

        });

        updateCartTotal();
    }


    initializeRows();


    document.addEventListener(
        "formset:added",
        function (event) {

            const row = event.target;

            addQuantityControls(row);
            addRemoveButton(row);

            updateCartTotal();
        }
    );

});