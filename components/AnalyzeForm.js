"use client"
import { useState } from 'react'
import styles from '../styles/Home.module.css'

export default function AnalyzeForm() {
  const [prompt, setPrompt] = useState('')
  const [file, setFile] = useState(null)
  const [resultUrl, setResultUrl] = useState('')
  const API_BASE = 'http://127.0.0.1:8000' // ganti sesuai backend

  const handleSubmit = async (e) => {
    e.preventDefault()
    setResultUrl('')

    const formData = new FormData()
    formData.append('prompt', prompt)
    if (file) formData.append('upload_file', file)

    try {
      const res = await fetch(`${API_BASE}/analyze/`, {
        method: 'POST',
        body: formData
      })

      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      const blob = await res.blob()
      setResultUrl(URL.createObjectURL(blob))
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <input
        className={styles.input}
        type="text"
        placeholder="Enter prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        required
      />
      <input
        className={styles.input}
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button className={styles.button} type="submit">Analyze</button>

      {resultUrl && (
        <img
          src={resultUrl}
          alt="Analysis Result"
          className={styles.resultImage}
        />
      )}
    </form>
  )
}
