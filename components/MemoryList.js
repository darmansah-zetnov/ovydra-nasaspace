"use client"
import { useEffect, useState } from 'react'
import styles from '../styles/Home.module.css'

export default function MemoryList() {
  const [memory, setMemory] = useState([])
  const API_BASE = 'http://127.0.0.1:8000'

  const fetchMemory = async () => {
    try {
      const res = await fetch(`${API_BASE}/memory/`)
      if (!res.ok) throw new Error(res.status)
      const data = await res.json()
      setMemory(data)
    } catch (err) {
      console.error('Memory fetch error', err)
    }
  }

  useEffect(() => {
    fetchMemory()
    const interval = setInterval(fetchMemory, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <ul className={styles.memoryList}>
      {memory.length === 0 ? <li className={styles.memoryItem}>No memory yet</li> :
        memory.map((item, idx) => (
          <li key={idx} className={styles.memoryItem}>
            Prompt: {item.prompt} → Response: {item.response}
          </li>
        ))
      }
    </ul>
  )
}
