import React from "react";

interface Props {
  close: boolean;
  onClose(): void;
  onDownload(): void;
}

const EmptyFieldsModal: React.FC<Props> = ({ close, onClose, onDownload }) => {
  function clickDownload() {
    onDownload();
    onClose();
  }

  if (close === true) {
    return null;
  } else
    return (
      <>
        <div className="overlay">
          <div className="modalContainer black fw6 br2 pb2 pt3">
            <p>
              You are about to download an incomplete form. Do you want to
              continue?
            </p>
            <div className="buttonContainer">
              <button
                onClick={clickDownload}
                className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc"
              >
                <span>Download</span>
              </button>
              <button
                onClick={onClose}
                className="ba bw2 b--light-gray bg-white black bg-animate hover-bg-light-gray fw6 db w-100 br2 pv3 ph4 mb4 tc"
              >
                <span>Cancel</span>
              </button>
            </div>
          </div>
        </div>
      </>
    );
};

export default EmptyFieldsModal;
