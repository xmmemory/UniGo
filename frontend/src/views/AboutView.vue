<template>
  <div class="about">
    <h1>关于我们</h1>
    <div class="about-content">
      <section class="about-section">
        <h2>UniGo 学生拼车平台</h2>
        <p>
          UniGo 是一个专为学生设计的拼车平台，旨在帮助学生更安全、便捷、经济地共享出行。
          我们致力于为学生提供一个可靠的拼车服务，让出行变得更加简单和环保。
        </p>
      </section>

      <section class="about-section">
        <h2>我们的使命</h2>
        <p>
          通过技术创新和优质服务，连接有出行需求的学生，提供安全、便捷、经济的拼车解决方案，
          促进校园社区的可持续发展。
        </p>
      </section>

      <section class="about-section">
        <h2>核心功能</h2>
        <ul>
          <li>✅ 安全可靠的实名认证系统</li>
          <li>✅ 便捷的行程发布和搜索功能</li>
          <li>✅ 智能匹配算法，快速找到合适的拼车伙伴</li>
          <li>✅ 透明的价格体系和安全保障</li>
          <li>✅ 实时聊天功能，方便沟通</li>
          <li>✅ 评价系统，建立信任机制</li>
        </ul>
      </section>

      <section class="about-section">
        <h2>联系方式</h2>
        <p>如果您有任何问题或建议，请通过以下方式联系我们：</p>
        <ul>
          <li>📧 邮箱: support@unigo.com</li>
          <li>📞 电话: 400-123-4567</li>
          <li>📍 地址: 北京市海淀区中关村大街1号</li>
        </ul>
      </section>
    </div>
  </div>
</template>

<style scoped>
.about {
  padding: 1rem 0;
}

.about-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.about-section {
  margin-bottom: 1.5rem;
}

.about-section h2 {
  color: #42b883;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.about-section p {
  line-height: 1.6;
  color: #333;
  font-size: 0.95rem;
}

.about-section ul {
  padding-left: 1.2rem;
}

.about-section li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* 平板和桌面端适配 */
@media (min-width: 768px) {
  .about {
    padding: 2rem 0;
  }
  
  .about-content {
    padding: 0 2rem;
  }
  
  .about-section {
    margin-bottom: 2rem;
  }
  
  .about-section h2 {
    font-size: 1.5rem;
  }
  
  .about-section p, .about-section li {
    font-size: 1rem;
  }
  
  .about-section ul {
    padding-left: 1.5rem;
  }
}
</style>