import { mount } from '@vue/test-utils'
import HomePage from '@/components/HomePage.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { vi } from 'vitest'

const mockRoutes = [
  { path: '/detail/:id', name: 'DetailPage', component: { template: '<div>Detail</div>' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes: mockRoutes
})

describe('HomePage.vue', () => {
  beforeEach(async () => {
    router.push('/')
    await router.isReady()
  })

  it('Renders all train lines by default', () => {
    const wrapper = mount(HomePage, {
      global: { plugins: [router] }
    })
    expect(wrapper.findAll('.card').length).toBe(8)
  })

  it('Filters train lines based on search query', async () => {
    const wrapper = mount(HomePage, {
      global: { plugins: [router] }
    })
    const input = wrapper.find('input')
    await input.setValue('BTS')
    const cards = wrapper.findAll('.card')
    expect(cards.length).toBe(1)
    expect(cards[0].text()).toContain('BTS (Green line)')
  })

  it('Shows no results message when no match', async () => {
    const wrapper = mount(HomePage, {
      global: { plugins: [router] }
    })
    await wrapper.find('input').setValue('XYZ')
    expect(wrapper.text()).toContain('No matching train line found!')
  })

  it('Navigates to detail page on View button click', async () => {
    const pushSpy = vi.spyOn(router, 'push')
    const wrapper = mount(HomePage, {
      global: { plugins: [router] }
    })
    const buttons = wrapper.findAll('button')
    const viewButton = buttons.find(btn => btn.text() === 'View')
    expect(viewButton).toBeTruthy()
    await viewButton.trigger('click')
    expect(pushSpy).toHaveBeenCalledWith('/detail/1')
  })
})
