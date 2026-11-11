import { getApp, getApps, initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: 'AIzaSyCRluT6lAo5qLBWijsUxfzoSiC_kx6o-qw',
  authDomain: 'suresh-d1164.firebaseapp.com',
  projectId: 'suresh-d1164',
  storageBucket: 'suresh-d1164.firebasestorage.app',
  messagingSenderId: '464452227902',
  appId: '1:464452227902:web:f30bcd39211441b13e526f',
  measurementId: 'G-7B01BW5PNN'
}

const app = getApps().length ? getApp() : initializeApp(firebaseConfig)
export const db = getFirestore(app)
