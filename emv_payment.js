   /**

    * _call_emv - sends the data to the back-end's function the establishes a connection to the terminal

    * emv_pay_data - prepares the relevant data (Json) to send to the terminal

    * _emv_handle_response - handles the response from the terminal and acts/responds to the user accordingly. 

    */   

    _emv_pay: function () {

        var self = this;
 
        var line = this.pos.get_order().selected_paymentline;

 
       
 
        // initializing a field representing the num of payments, by default it should be 1.
 
        line.num_of_payments = 1;
        
        // num_of_payments = the number of payments selected by the user in the UI 
        // installment_amount = amount of each installment of the user chose to divide the payment.
        // total_amount = the total amount of all the installments
 
        if (line.amount < 0) {
            //refunds should still be in one installment 
            var data = this._emv_refund_data();
 
        }
        else if(num_of_payments > 1) {
            line.amount = installment_amount ;;
            total_amount -= installment_amount;;
            num_of_payments --;
        
            /* set the line.amount (the amount to be charged) as the installment amount and
            pay only for the first installment. By doing this we can keep track of the amount of
            payments left to handle, and set up the backend to execute the remaining payments in 1 month intervals
            until num_of_payments = 1 and then we would finish the payment procedure. */
           
            var data = this._emv_pay_data()

        }
        else{
 
            var data = this._emv_pay_data();
 
        }
 
  
 
        return this._call_emv(data).then(function (data) {
 
            return self._emv_handle_response(data);
 
        });
 
    },
 
 
 
 
  
 
    /**
 
     * Called when a user clicks the "Send" button in the
 
     * interface. This should initiate a payment request and return a
 
     * Promise that resolves when the final status of the payment line
 
     * is set with set_payment_status.
 
     * 
 
     * @param {string} cid - The id of the paymentline
 
     * @returns {Promise} resolved with a boolean that is false when
 
     * the payment should be retried. Rejected when the status of the
 
     * paymentline will be manually updated.
 
     */
 
    send_payment_request: function (cid) {
 
        this._super.apply(this, arguments);
 
        this.pos.get_order().selected_paymentline.set_payment_status('waitingCard');
 
        return this._emv_pay();
    }


    // Not so sure I understood this task, if I did indeed misunderstand, I will gladly do the task again if needed.