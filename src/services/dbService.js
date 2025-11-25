// Serviço para comunicação com o banco de dados PostgreSQL
// Esta é uma camada de abstração que pode ser usada com um backend API

// URL da API - verifica em ordem: window.API_URL (Hostgator), env var, ou localhost
const API_BASE_URL = (typeof window !== 'undefined' && window.API_URL) 
  ? window.API_URL 
  : (import.meta.env.VITE_API_URL || 'http://localhost:8002/api')

// Função auxiliar para fazer requisições (inclui token de autenticação)
async function fetchAPI(endpoint, options = {}) {
  // Obter token de autenticação do localStorage
  const token = localStorage.getItem('auth_token')
  
  // Log para debug
  if (endpoint.includes('/ideias') && options.method === 'POST') {
    console.log('🔐 [dbService] Criando ideia - Token presente:', !!token)
    if (token) {
      console.log('   Token (primeiros 20 chars):', token.substring(0, 20) + '...')
    } else {
      console.warn('   ⚠️  ATENÇÃO: Token não encontrado no localStorage!')
    }
  }
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }
  
  // Adicionar token de autenticação se existir
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  } else {
    console.warn('⚠️  [dbService] Requisição sem token de autenticação:', endpoint)
  }
  
  try {
    // Garantir que método GET seja explícito para buscar ideias
    const method = options.method || (endpoint === '/ideias' ? 'GET' : undefined)
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: method,
      headers,
      ...options,
    })

    // Verificar se a resposta é JSON
    const contentType = response.headers.get('content-type')
    if (!contentType || !contentType.includes('application/json')) {
      const text = await response.text()
      console.error('Resposta não é JSON:', text.substring(0, 200))
      throw new Error(`Backend retornou resposta inválida: ${response.status} ${response.statusText}`)
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Erro na API: ${response.statusText} (${response.status})`)
    }

    return await response.json()
  } catch (error) {
    console.error('Erro ao comunicar com a API:', error)
    throw error
  }
}

// Buscar todas as ideias
export async function buscarTodasIdeias() {
  try {
    const resultado = await fetchAPI('/ideias')
    // Se obteve sucesso, limpar localStorage para não confundir
    localStorage.removeItem('sacola_ideias')
    return resultado
  } catch (error) {
    console.error('Erro ao buscar ideias da API:', error)
    // Não usar fallback - sempre lançar erro para mostrar que API não está funcionando
    throw error
  }
}

// Buscar ideia por ID
export async function buscarIdeiaPorId(id) {
  try {
    return await fetchAPI(`/ideias/${id}`)
  } catch (error) {
    console.error('Erro ao buscar ideia:', error)
    throw error
  }
}

// Salvar nova ideia
export async function salvarIdeia(ideia) {
  try {
    const payload = {
      titulo: ideia.titulo,
      tag: ideia.tag || null,
      ideia: ideia.ideia
    }
    
    // Se tiver embedding, usar endpoint específico
    if (ideia.embedding && Array.isArray(ideia.embedding)) {
      return await fetchAPI('/ideias/com-embedding', {
        method: 'POST',
        body: JSON.stringify({
          ideia: payload,
          embedding: ideia.embedding
        }),
      })
    }
    
    return await fetchAPI('/ideias', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  } catch (error) {
    console.error('Erro ao salvar ideia:', error)
    throw error // Não usar localStorage como fallback, deixar o erro subir
  }
}

// Atualizar ideia existente
export async function atualizarIdeia(id, ideiaAtualizada) {
  try {
    return await fetchAPI(`/ideias/${id}`, {
      method: 'PUT',
      body: JSON.stringify(ideiaAtualizada),
    })
  } catch (error) {
    console.error('Erro ao atualizar ideia:', error)
    // Fallback para localStorage se API não disponível
    const ideias = JSON.parse(localStorage.getItem('sacola_ideias') || '[]')
    const index = ideias.findIndex(i => i.id === id)
    if (index !== -1) {
      ideias[index] = { ...ideias[index], ...ideiaAtualizada }
      localStorage.setItem('sacola_ideias', JSON.stringify(ideias))
      return ideias[index]
    }
    throw new Error('Ideia não encontrada')
  }
}

// Deletar ideia
export async function deletarIdeia(id) {
  try {
    return await fetchAPI(`/ideias/${id}`, {
      method: 'DELETE',
    })
  } catch (error) {
    console.error('Erro ao deletar ideia:', error)
    // Fallback para localStorage se API não disponível
    const ideias = JSON.parse(localStorage.getItem('sacola_ideias') || '[]')
    const filtradas = ideias.filter(i => i.id !== id)
    localStorage.setItem('sacola_ideias', JSON.stringify(filtradas))
    return { success: true }
  }
}

// Buscar por similaridade (backend gera embedding automaticamente)
export async function buscarPorSimilaridade(termoBusca) {
  try {
    // Backend gera embedding automaticamente, só enviar o termo
    return await fetchAPI('/ideias/buscar', {
      method: 'POST',
      body: JSON.stringify({
        termo: termoBusca,
      }),
    })
  } catch (error) {
    console.error('Erro na busca por similaridade:', error)
    throw error
  }
}

// Salvar ideia com embedding
export async function salvarIdeiaComEmbeddingDB(ideia, embedding, apiKey) {
  try {
    return await fetchAPI('/ideias/com-embedding', {
      method: 'POST',
      body: JSON.stringify({
        ideia: ideia,
        embedding: embedding,
      }),
    })
  } catch (error) {
    console.error('Erro ao salvar ideia com embedding:', error)
    throw error
  }
}

// Atualizar embedding de uma ideia
export async function atualizarEmbedding(id, embedding) {
  try {
    return await fetchAPI(`/ideias/${id}/embedding`, {
      method: 'PUT',
      body: JSON.stringify({ embedding }),
    })
  } catch (error) {
    console.error('Erro ao atualizar embedding:', error)
    throw error
  }
}

