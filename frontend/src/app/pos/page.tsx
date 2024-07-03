"use client"
import React, { useEffect, useState } from 'react';
import fetchProducts from "./fetchProducts";
import createTransaction from "./createTransaction";
// import styles from '../styles/Home_modules.css';

type Product = {
  name: string;
  quantity: number;
  price: string;
  totalprice: string;
};

export default function Home() {
  const [productCode, setProductCode] = useState('');
  const [productName, setProductName] = useState('');
  const [productPrice, setProductPrice] = useState('');
  const [purchaseList, setPurchaseList] = useState<Product[]>([]);

  const handleProductCodeRead = async () => {
    try {
      const productInfos = await fetchProducts(productCode);
      console.log(productInfos);
      const displayProductInfo = productInfos[0];

      if (Array.isArray(displayProductInfo) && displayProductInfo.length > 0) {
        setProductName(displayProductInfo[0].NAME);
        setProductPrice(displayProductInfo[0].PRICE);
      } else {
        setProductName('商品がマスタ未登録です');
      }
    } catch (error) {
      console.error("Error handling product code read:", error);
    }
  };

  const addItem = () => {
    if (!productPrice) {
      setProductName('');
      setProductPrice('');
    } else {
      // console.log(...purchaseList);
      setPurchaseList([
        ...purchaseList,
        { name: productName, quantity: 1, price: productPrice, totalprice: productPrice },
      ]);
      setProductCode('');
      setProductName('');
      setProductPrice('');
    }
  };

  // const calculateTotalPrice = () => {
  //   return purchaseList.reduce((total, item) => total + item.totalprice, 0);
  // };
  
  const handlePurchase = async () => {
    try {
      const totalPrice = await createTransaction(purchaseList);
      const tax = 1.1
      alert(`合計金額は ${totalPrice*tax} 円です`);
      setProductCode('');
      setProductName('');
      setProductPrice('');
      setPurchaseList([]);
    } catch (error) {
      console.error("Purchase failed:", error);
    }
  };

  return (
    <>
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', display: 'flex' }}>
        <div style={{ flex: 1, padding: '30px' }}>
          <div>
            <input
              type="text"
              value={productCode}
              onChange={(e) => setProductCode(e.target.value)}
              placeholder="商品コード"
              style={{ width: '100%', padding: '10px', marginBottom: '10px', border: '2px solid', textAlign: 'center' }}
            />
            <button
              onClick={handleProductCodeRead}
              style={{ width: '100%', padding: '10px', marginBottom: '20px', backgroundColor: 'lightblue', border: '3px solid black', fontWeight: 'bold' }}
            >
              商品コード 読み込み
            </button>
          </div>
          <div style={{ paddingTop: '30px' }}>
            <input
              type="text"
              value={productName}
              readOnly
              placeholder="商品名"
              // className={styles.inputField}
              style={{ width: '100%', padding: '10px', marginBottom: '10px', backgroundColor: 'inherit', border: '2px solid black', textAlign: 'center' }}
            />
            <input
              type="text"
              value={productPrice}
              readOnly
              placeholder="価格"
              style={{ width: '100%', padding: '10px', marginBottom: '10px', backgroundColor: 'inherit', border: '2px solid black', textAlign: 'center' }}
            />
            <button
              onClick={addItem}
              style={{ width: '100%', padding: '10px', marginBottom: '20px', backgroundColor: 'lightblue', border: '3px solid black', fontWeight: 'bold' }}
            >
              追加
            </button>
          </div>
        </div>
        <div style={{ flex: 1, padding: '30px' }}>
          <div>
            <h3 style={{ textAlign: 'center', paddingBottom: '10px' }} >購入リスト</h3>
            <ul style={{ listStyle: 'none', padding: '10px', backgroundColor: 'inherit', border: '2px solid black' }}>
              {purchaseList.length > 0 ? (
                purchaseList.map((item, index) => (
                  <li key={index} style={{ marginBottom: '10px' }}>
                    {item.name} x {item.quantity} {item.price}円 {item.totalprice}円
                  </li>
                ))
              ) : (
                <li style={{ marginBottom: '10px', color: 'grey' }}>No items in the purchase list</li>
              )}
            </ul>
            <button
              onClick={handlePurchase}
              style={{ width: '100%', padding: '10px', marginTop: '10px', backgroundColor: 'lightblue', border: '3px solid black', fontWeight: 'bold' }}
            >
              購入
            </button>
          </div>
        </div>
      </div>
    </>
  );
};