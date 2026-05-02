import { createRouter, createWebHistory } from 'vue-router'

import ColorsView from '../../views/ColorsView.vue'
import DatesView from '../../views/DatesView.vue'
import DocumentsView from '../../views/DocumentsView.vue'
import FakeDataView from '../../views/FakeDataView.vue'
import FilesView from '../../views/FilesView.vue'
import HashView from '../../views/HashView.vue'
import HomeView from '../../views/HomeView.vue'
import ImagesView from '../../views/ImagesView.vue'
import JsonView from '../../views/JsonView.vue'
import LinksView from '../../views/LinksView.vue'
import MarkdownView from '../../views/MarkdownView.vue'
import MediaView from '../../views/MediaView.vue'
import MessagesView from '../../views/MessagesView.vue'
import PasswordsView from '../../views/PasswordsView.vue'
import PdfView from '../../views/PdfView.vue'
import QrCodeView from '../../views/QrCodeView.vue'
import SignatureView from '../../views/SignatureView.vue'
import SlugView from '../../views/SlugView.vue'
import TextView from '../../views/TextView.vue'
import UnitsView from '../../views/UnitsView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/qrcode',
      name: 'qrcode',
      component: QrCodeView,
    },
    {
      path: '/passwords',
      name: 'passwords',
      component: PasswordsView,
    },
    {
      path: '/json',
      name: 'json',
      component: JsonView,
    },
    {
      path: '/documents',
      name: 'documents',
      component: DocumentsView,
    },
    {
      path: '/slug',
      name: 'slug',
      component: SlugView,
    },
    {
      path: '/text',
      name: 'text',
      component: TextView,
    },
    {
      path: '/hash',
      name: 'hash',
      component: HashView,
    },
    {
      path: '/dates',
      name: 'dates',
      component: DatesView,
    },
    {
      path: '/images',
      name: 'images',
      component: ImagesView,
    },
    {
      path: '/links',
      name: 'links',
      component: LinksView,
    },
    {
      path: '/files',
      name: 'files',
      component: FilesView,
    },
    {
      path: '/units',
      name: 'units',
      component: UnitsView,
    },
    {
      path: '/colors',
      name: 'colors',
      component: ColorsView,
    },
    {
      path: '/markdown',
      name: 'markdown',
      component: MarkdownView,
    },
    {
      path: '/fake-data',
      name: 'fake-data',
      component: FakeDataView,
    },
    {
      path: '/signature',
      name: 'signature',
      component: SignatureView,
    },
    {
      path: '/messages',
      name: 'messages',
      component: MessagesView,
    },
    {
      path: '/pdf',
      name: 'pdf',
      component: PdfView,
    },
    {
      path: '/media',
      name: 'media',
      component: MediaView,
    },
  ],
})
