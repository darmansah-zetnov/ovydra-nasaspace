import AnalyzeForm from '../components/AnalyzeForm'
import MemoryList from '../components/MemoryList'
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Ovydra AI - Exoplanet Analysis</h1>
      <AnalyzeForm />
      <h2 className={styles.subtitle}>Memory / History</h2>
      <MemoryList />
    </div>
  )
}
