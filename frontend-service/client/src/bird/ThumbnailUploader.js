import React, { useState } from 'react';
import axios from 'axios';

export function ThumbnailUploader({ bird }) {
  const [file, setFile] = useState(null);
  const [credit, setCredit] = useState('');
  let fileInputRef = React.createRef();
  const handleFileInput = event => {
    event.preventDefault();
    setFile(fileInputRef.current.files[0]);
  };
  const uploadFile = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('picture', file);
    formData.append('credit', credit);
    const response = await axios.post(`/api/pictures`, formData);
    if (response.status === 200) {
      const json = response.data;
    }
    setFile(null);
  };
  const selectFile = async (event) => {
    event.preventDefault();
    fileInputRef.current.click();
  };
  const handleCreditChange = event => {
    setCredit(event.target.value);
  };
  return (<form>
    <input type='file' accept='image/*' style={{ display: 'none' }} onChange={handleFileInput} ref={fileInputRef} />
    <button id='fileSelect' onClick={selectFile}>Select bird thumbnail</button>
    <label>Credit</label>
    <input type='text' vanlue={credit} onChange={handleCreditChange} />
    {file && file.name}
    {file && <button onClick={uploadFile}>Upload</button>}
  </form>);
}
