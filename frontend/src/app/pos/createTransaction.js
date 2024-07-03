"use server";
import { revalidatePath } from 'next/cache';


const createTransaction = async (purchaseList) => {

    // const body_msg = JSON.stringify({ purchaseList });
    // console.log(req);

    const transactionRequest = {
        emp_cd: 9999999999,
        store_cd: 30,
        pos_no: 90,
        total_amt: 0,
        transaction: purchaseList,
    };


    try {
        const res = await fetch(process.env.API_ENDPOINT+'/transactions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            // body: body_msg,
            body: JSON.stringify(transactionRequest),
        });
        // console.log(res);


        if (!res.ok) {
            const errorText = await res.text();  // レスポンスをテキストとして取得
            console.error('Error details:', errorText);
            throw new Error(`Failed to create Transaction: ${res.status} ${res.statusText}`);
        }

        const responseData = await res.json();
        // console.log(responseData);
        return responseData[0].total_amt;

    } catch (error) {
        console.error('Error creating transaction:', error);
        throw error;
    }
}

export default createTransaction;