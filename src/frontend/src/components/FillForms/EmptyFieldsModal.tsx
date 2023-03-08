import React from "react";

interface Props {
  close: boolean;
  onClose(): void;
  onDownload(): void;
}

const EmptyFieldsModal: React.FC<Props> = ({
  close,
  onClose,
  onDownload,
}: Props): JSX.Element | null => {
  function clickDownload() {
    onDownload();
    onClose();
  }

  return !close ? (
    <div className="fixed top-0 bottom-0 left-0 right-0 z-9999 bg-black-30">
      <div className="modalContainer flex flex-column tc mw7 w-100 fixed z-9999 bg-white shadow-5 black f6 f5-l fw6 br2 pb2 pt3">
        <p>
          You are about to download an incomplete form. Do you want to continue?
        </p>
        <div className="flex justify-center pa2 mt3">
          <button
            onClick={clickDownload}
            className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 tc w-100 ma2"
          >
            Download
          </button>
          <button
            onClick={onClose}
            className="ba bw2 b--light-gray bg-white black bg-animate hover-bg-light-gray fw6 db w-100 br2 pv3 ph4 tc w-100 ma2"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  ) : null;
};

export default EmptyFieldsModal;
