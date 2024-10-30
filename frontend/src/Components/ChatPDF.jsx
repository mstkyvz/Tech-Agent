import React, { useEffect, useState } from 'react';
import { Document, Page, Text, View, StyleSheet, Image } from '@react-pdf/renderer';
import {unified} from 'unified';
import remarkParse from 'remark-parse';
import remarkMath from 'remark-math';
import rehypeParse from 'rehype-parse';
import rehypeStringify from 'rehype-stringify';
import rehypeKatex from 'rehype-katex';


// Styles for PDF document
const styles = StyleSheet.create({
  page: {
    padding: 30,
    backgroundColor: '#ffffff',
  },
  message: {
    marginBottom: 20,
    padding: 10,
    borderRadius: 5,
  },
  userMessage: {
    backgroundColor: '#f3f4f6',
    marginLeft: '20%',
  },
  assistantMessage: {
    backgroundColor: '#ffffff',
    marginRight: '20%',
    border: '1px solid #e5e7eb',
  },
  messageText: {
    fontSize: 12,
    lineHeight: 1.5,
  },
  image: {
    marginBottom: 10,
    maxWidth: '100%',
    maxHeight: 200,
    objectFit: 'contain',
  },
  timestamp: {
    fontSize: 10,
    color: '#666666',
    marginTop: 5,
  },
});

// Helper function to process markdown content
const processMarkdown = async (content) => {
  const processor = unified()
    .use(remarkParse)
    .use(remarkMath)
    .use(rehypeParse, { fragment: true })
    .use(rehypeKatex)
    .use(rehypeStringify);

  const result = await processor.process(content);
  return String(result);
};

// Component to render markdown elements
const MarkdownElement = ({ content }) => (
  <Text style={styles.messageText} dangerouslySetInnerHTML={{ __html: content }} />
);

const ChatPDF = ({ messages }) => {
  const [processedMessages, setProcessedMessages] = useState([]);

  useEffect(() => {
    const processMessages = async () => {
      const processed = await Promise.all(messages.map(async (message) => {
        if (message.type === 'assistant') {
          const processedContent = await processMarkdown(message.content);
          return { ...message, processedContent };
        }
        return message;
      }));
      setProcessedMessages(processed);
    };

    processMessages();
  }, [messages]);

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        {processedMessages.map((message, index) => (
          <View key={index} style={[
            styles.message,
            message.type === 'user' ? styles.userMessage : styles.assistantMessage
          ]}>
            {message.image && (
              <Image
                src={message.image}
                style={styles.image}
              />
            )}
            {message.type === 'user' ? (
              <Text style={styles.messageText}>{message.content}</Text>
            ) : (
              <MarkdownElement content={message.processedContent} />
            )}
            <Text style={styles.timestamp}>
              {new Date(message.timestamp).toLocaleString()}
            </Text>
          </View>
        ))}
      </Page>
    </Document>
  );
};

export default ChatPDF;
