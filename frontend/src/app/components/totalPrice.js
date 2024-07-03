import React, { useState } from 'react';

const Modal = ({ isOpen, onClose, totalPrice }) => {
  if (!isOpen) return null;

  return (
    <div style={modalStyles.overlay}>
      <div style={modalStyles.modal}>
        <h2 style={{ fontSize: '24px' }}>合計金額は {totalPrice} 円です</h2>
        <button onClick={onClose} style={modalStyles.button}>閉じる</button>
      </div>
    </div>
  );
};

const modalStyles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modal: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
  },
  button: {
    marginTop: '20px',
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
  },
};

const App = () => {
  const [purchaseList, setPurchaseList] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [totalPrice, setTotalPrice] = useState(0);

  const calculateTotalPrice = () => {
    return purchaseList.reduce((total, item) => total + item.totalprice, 0);
  };

  const handlePurchase = () => {
    const totalPrice = calculateTotalPrice();
    setTotalPrice(totalPrice);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div>
      {/* その他のコンポーネント部分 */}
      <button onClick={handlePurchase}>購入</button>
      <Modal isOpen={isModalOpen} onClose={closeModal} totalPrice={totalPrice} />
    </div>
  );
};

export default App;
