import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image } from '@react-pdf/renderer';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import { renderToStaticMarkup } from 'react-dom/server';

// Define styles for PDF document
const styles = StyleSheet.create({
  page: {
    padding: 30,
    backgroundColor: '#ffffff'
  },
  header: {
    marginBottom: 20,
    borderBottom: 1,
    borderBottomColor: '#e5e7eb',
    paddingBottom: 10
  },
  headerText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#374151'
  },
  message: {
    marginBottom: 20,
    padding: 10,
    borderRadius: 5
  },
  userMessage: {
    backgroundColor: '#f3f4f6',
    marginLeft: '20%',
  },
  assistantMessage: {
    backgroundColor: '#ffffff',
    marginRight: '20%',
    border: 1,
    borderColor: '#e5e7eb',
  },
  messageText: {
    fontSize: 12,
    lineHeight: 1.5,
    wordBreak: 'break-word'
  },
  image: {
    marginBottom: 10,
    maxWidth: '100%',
    maxHeight: 200,
    objectFit: 'contain'
  },
  timestamp: {
    fontSize: 10,
    color: '#666666',
    marginTop: 5,
    textAlign: 'right'
  },
  metaInfo: {
    fontSize: 10,
    color: '#666666',
    marginBottom: 5
  },
  pageNumber: {
    position: 'absolute',
    bottom: 30,
    left: 0,
    right: 0,
    textAlign: 'center',
    fontSize: 10,
    color: '#666666'
  },
  codeBlock: {
    fontFamily: 'Courier',
    backgroundColor: '#f7f7f7',
    padding: 8,
    marginVertical: 5,
    fontSize: 10
  }
});

// Custom Markdown components for PDF rendering
const MarkdownComponents = {
  p: ({ children }) => <Text style={{ marginBottom: 10 }}>{children}</Text>,
  h1: ({ children }) => <Text style={{ fontSize: 16, fontWeight: 'bold', marginVertical: 10 }}>{children}</Text>,
  h2: ({ children }) => <Text style={{ fontSize: 14, fontWeight: 'bold', marginVertical: 8 }}>{children}</Text>,
  h3: ({ children }) => <Text style={{ fontSize: 12, fontWeight: 'bold', marginVertical: 6 }}>{children}</Text>,
  code: ({ inline, children }) => (
    inline ? 
      <Text style={{ fontFamily: 'Courier', backgroundColor: '#f7f7f7', padding: 2 }}>{children}</Text> :
      <View style={styles.codeBlock}>
        <Text>{children}</Text>
      </View>
  ),
  ul: ({ children }) => <View style={{ marginLeft: 20, marginVertical: 5 }}>{children}</View>,
  ol: ({ children }) => <View style={{ marginLeft: 20, marginVertical: 5 }}>{children}</View>,
  li: ({ children }) => <Text style={{ marginBottom: 5 }}>• {children}</Text>,
  blockquote: ({ children }) => (
    <View style={{ borderLeftWidth: 2, borderLeftColor: '#e5e7eb', paddingLeft: 10, marginVertical: 5 }}>
      <Text style={{ fontStyle: 'italic' }}>{children}</Text>
    </View>
  ),
};

const processMessageContent = (content) => {
  if (typeof content !== 'string') return content;

  // Render markdown content
  const markdownContent = (
    <ReactMarkdown
      remarkPlugins={[remarkMath, remarkGfm]}
      rehypePlugins={[rehypeKatex]}
      components={MarkdownComponents}
    >
      {content}
    </ReactMarkdown>
  );

  // Convert to static markup
  return renderToStaticMarkup(markdownContent);
};

const ChatPDF = ({ messages, chatId }) => {
  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Group messages by date
  const groupMessagesByDate = () => {
    const groups = {};
    messages.forEach(message => {
      const date = new Date(message.timestamp).toLocaleDateString();
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push({
        ...message,
        content: message.type === 'user' ? message.content : processMessageContent(message.content)
      });
    });
    return groups;
  };

  const messageGroups = groupMessagesByDate();

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.header}>
          <Text style={styles.headerText}>Chat Transcript #{chatId}</Text>
          <Text style={styles.metaInfo}>
            Generated on: {new Date().toLocaleDateString()}
          </Text>
          <Text style={styles.metaInfo}>
            Total Messages: {messages.length}
          </Text>
        </View>

        {Object.entries(messageGroups).map(([date, dateMessages]) => (
          <View key={date} wrap={false}>
            <Text style={[styles.metaInfo, { marginTop: 10, fontWeight: 'bold' }]}>
              {date}
            </Text>

            {dateMessages.map((message, index) => (
              <View 
                key={index} 
                style={[
                  styles.message,
                  message.type === 'user' ? styles.userMessage : styles.assistantMessage
                ]}
                wrap={false}
              >
                <Text style={styles.metaInfo}>
                  {message.type === 'user' ? 'User' : 'Assistant'}
                </Text>

                {message.image && (
                  <Image
                    src={message.image}
                    style={styles.image}
                  />
                )}

                <Text style={styles.messageText}>
                  {message.content}
                </Text>

                <Text style={styles.timestamp}>
                  {formatDate(message.timestamp)}
                </Text>
              </View>
            ))}
          </View>
        ))}

        <Text 
          style={styles.pageNumber} 
          render={({ pageNumber, totalPages }) => (
            `${pageNumber} / ${totalPages}`
          )} 
        />
      </Page>
    </Document>
  );
};

export default ChatPDF;