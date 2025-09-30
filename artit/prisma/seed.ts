import { PrismaClient } from '@/app/generated/prisma'

const prisma = new PrismaClient()

async function main() {
  const articles = [
    {
      id: 'a1',
      title: "Qu'est-ce que l'EBITDA ?",
      date: new Date('2024-11-02'),
      summary: "Définition et intérêt pour l'analyse de performance."
    },
    {
      id: 'a2',
      title: 'Marge brute vs marge nette',
      date: new Date('2025-01-15'),
      summary: 'Comprendre les niveaux de marge et leurs usages.'
    },
    {
      id: 'a3',
      title: 'Flux de trésorerie opérationnel',
      date: new Date('2024-12-10'),
      summary: 'Analyse du cash flow des opérations courantes.'
    },
    {
      id: 'a4',
      title: 'Ratio de liquidité générale',
      date: new Date('2024-10-22'),
      summary: 'Mesure de la capacité à honorer ses dettes court terme.'
    },
    {
      id: 'a5',
      title: 'Return on Equity (ROE)',
      date: new Date('2025-01-20'),
      summary: 'Rentabilité des capitaux propres investis.'
    },
    {
      id: 'a6',
      title: 'Working Capital',
      date: new Date('2024-11-15'),
      summary: 'Besoin en fonds de roulement et gestion du cycle d\'exploitation.'
    },
    {
      id: 'a7',
      title: 'Dette nette et levier financier',
      date: new Date('2024-09-30'),
      summary: 'Comprendre l\'endettement et son impact sur la valorisation.'
    },
    {
      id: 'a8',
      title: 'Free Cash Flow (FCF)',
      date: new Date('2025-01-05'),
      summary: 'Cash flow libre après investissements nécessaires.'
    },
    {
      id: 'a9',
      title: 'Price to Earnings Ratio',
      date: new Date('2024-12-01'),
      summary: 'Valorisation boursière par rapport aux bénéfices.'
    },
    {
      id: 'a10',
      title: 'Goodwill et actifs incorporels',
      date: new Date('2024-10-10'),
      summary: 'Traitement comptable des acquisitions et survaleur.'
    }
  ]

  for (const article of articles) {
    await prisma.article.upsert({
      where: { id: article.id },
      update: {},
      create: article
    })
  }

  console.log('✅ Database seeded successfully')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
